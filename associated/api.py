from __future__ import unicode_literals

import base64
import hashlib

from django.db import transaction
from django.http.response import JsonResponse
from django.utils import timezone
from oidc_provider.models import Client
from werkzeug.exceptions import MethodNotAllowed, PreconditionFailed, Forbidden, NotImplemented

from associated.models import SimpleClientCommunicationRequest, AssociatedService
from library.log import rbe_logger

"""
    The general API for all associated services.
     The goal is that an associated service can send messages to users on a specific aggregation level.

     For example it can be send to all users with a specific country, with a distance to a specific location,
     or with a skill.

     The email comes from the RBE network and informs why the email is send and also generates an unsubscribe
     from this client link.
"""


@transaction.atomic
def simple_sendout(request):
    """ Makes a general sendout to every user on the network
        @required - client_id
        @message_text - the text that the people should receive """

    if request.method == 'POST':

        client_id = request.POST.get('client_id')

        try:
            client = Client.objects.get(client_id=client_id)
        except Client.DoesNotExist:
            rbe_logger.info(
                "Someone called the API for language_sendout with a not known client_id={}".format(client_id))
            return JsonResponse({'error': 'client_id not known'}, status=PreconditionFailed.code)

        message_text = request.POST.get('message_text')

        if not message_text or not (isinstance(message_text, str) or isinstance(message_text, unicode)):
            rbe_logger.info(
                "Someone called the API for language_sendout with a not known client_id={}".format(client_id))
            return JsonResponse({'error': 'message_text not valid'}, status=PreconditionFailed.code)

        if len(message_text) < 50:
            return JsonResponse({'error': 'message_text to short'}, status=PreconditionFailed.code)

        check_sum = request.POST.get('check_sum')

        if not check_sum:
            return JsonResponse({'error': 'check_sum not given'}, status=PreconditionFailed.code)

        # To verify that the client is really the one we check the message hash with salting by secret key
        dk = hashlib.pbkdf2_hmac('sha256', message_text, client.client_secret, 100000)
        check_sum_verification = base64.b64encode(dk).decode()  # py3k-mode

        if check_sum != check_sum_verification:
            rbe_logger.error("Checksum for request failed client_id={}".format(client.client_id))
            return JsonResponse({'error': 'check_sum not valid'}, status=Forbidden.code)

        # If all of those checks are passed we can actually check logical if the client is allowed to make
        # the request - we allow simplified one request every month for a given language

        # Lets check if there was a sendout on this language code

        try:
            assoc_net = AssociatedService.objects.get(client=client, enabled=True)
        except AssociatedService.DoesNotExist:
            rbe_logger.error(
                "Client requested sendout but assoc service not existing client_id={}".format(client.client_id))
            return JsonResponse({'error': 'Server has encountered internal precondition problems. '
                                           'Please contact the team that gave you the access to this service.'},
                                status=NotImplemented.code)

        minimal_sendout_date = timezone.datetime.now() - timezone.timedelta(days=assoc_net.sendout_day_period)

        # Check if there is something newer than the n-days silence period or a still pending request
        scc_qs_time = SimpleClientCommunicationRequest.objects.filter(client=client, pending=False, created__gte=minimal_sendout_date)
        scc_qs_pend = SimpleClientCommunicationRequest.objects.filter(client=client, pending=True)

        if scc_qs_pend.exists():
            # We cannot allow the client to send something again as there is still a job pending
            sccr = scc_qs_pend.first()
            return JsonResponse({
                'error': 'pending_job',
                'job_id': sccr.id,
                'job_created': sccr.created.isoformat()
            }, status=409)
        elif scc_qs_time.exists():
            # We cannot allow the client to send something again as they need to wait more time
            sccr = scc_qs_time.first()
            time_to_send_again = timezone.timedelta(days=assoc_net.sendout_day_period) - (timezone.now() - sccr.created)
            return JsonResponse({
                'error': 'timeout_period',
                'job_timeout': time_to_send_again.seconds
            }, status=409)
            pass
        else:
            # Create a job as the information send out needs to be quickly checked
            # Send a test email to the admin and present how the email would look like
            sccr = SimpleClientCommunicationRequest(client=client, message_text=message_text)
            sccr.save()

            return JsonResponse({
                'success': True,
                'job_id': sccr.id,
                'job_created': sccr.created.isoformat(),
                'job_description': 'The message was accepted and wil be checked. Once released it will be send to the desired group of users'
            }, status=202)

    else:
        return JsonResponse({'success': False}, status=MethodNotAllowed.code)
