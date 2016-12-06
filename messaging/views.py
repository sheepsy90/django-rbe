from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models.aggregates import Count
from django.http.response import JsonResponse, Http404
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from core.models import LastSeen
from library.log import rbe_logger
from messaging.models import Message, MessageStatus


@login_required()
def messages(request):
    qs = Message.objects.filter(recipient=request.user, status=MessageStatus.UNREAD).annotate(count=Count('status')).order_by('count')

    if not qs.exists():
        qs = Message.objects.filter(recipient=request.user).order_by('-sent_time')

    if not qs.exists():
        sender = LastSeen.objects.all().order_by('date_time').first()
    else:
        sender = qs.first().sender

    return conversation(request, sender.id)


def get_ordered_latest_contact_list(user):
    # TODO add distinct once switching to Postgresql
    sent_message = list(Message.objects.filter(sender=user).order_by('-sent_time').values_list('recipient', 'sent_time'))
    received_messages = list(Message.objects.filter(recipient=user).order_by('-sent_time').values_list('sender', 'sent_time'))

    result_dict = {}
    # Dummy algorithm to order by latest message
    for element in sent_message + received_messages:
        uid, dt = element

        if uid not in result_dict:
            result_dict[uid] = []
        result_dict[uid].append(dt)

    for key in result_dict.keys():
        result_dict[key] = max(result_dict[key])

    as_real_user_object = [(User.objects.get(id=e[0]), e[1]) for e in result_dict.items()]
    as_real_user_object = [{
        'user': e[0],
        'unread_messages': Message.objects.filter(sender=e[0], recipient=user, status=MessageStatus.UNREAD).count(),
        'last_contact': e[1]
    } for e in as_real_user_object]

    sorted_list = sorted(as_real_user_object, key=lambda x: (x['unread_messages'], x['last_contact']))
    sorted_list.reverse()
    return sorted_list


@login_required()
def conversation(request, user_id, error_message=''):
    try:
        rc = RequestContext(request)
        conversation_partner = User.objects.get(id=user_id)
        messages = Message.objects.filter(Q(sender=request.user) | Q(recipient=request.user)).filter(
            Q(sender=conversation_partner) | Q(recipient=conversation_partner)).order_by('-sent_time')

        ordered_latest_conversations = get_ordered_latest_contact_list(request.user)

        rc['latest_conversations'] = ordered_latest_conversations
        rc['messages'] = messages.reverse()
        rc['error_message'] = error_message
        rc['conversation_partner'] = conversation_partner
        return render_to_response('messaging/conversation.html', rc)
    except User.DoesNotExist:
        raise Http404


@login_required()
def send(request):
    recipient_id = request.POST.get('recipient_id')
    message_text = request.POST.get('message_text')
    error_message = ''

    try:
        if not message_text:
            error_message = 'Empty message cannot be sent!'
        elif len(message_text) > 1200:
            error_message = 'A message cannot be longer than 1200 characters!'
        else:
            recipient = User.objects.get(id=recipient_id)
            Message.create_message(request.user, recipient, message_text)
            return redirect(reverse('conversation', kwargs={'user_id': recipient.id}))
    except User.DoesNotExist as e:
        rbe_logger.warning("Had problems")
        error_message = "User to write to doesn't exists"
    except Exception as e:
        error_message = "Unknown error occurred - please try again later"
        rbe_logger.exception(e)

    return conversation(request, recipient_id, error_message)


@login_required()
def messaging_confirm_read(request):
    message_ids = request.POST.getlist('message_ids[]', None)

    if not message_ids:
        return JsonResponse({'success': False, 'reason': 'No message_ids list present'})

    try:
        message_ids = [int(e) for e in message_ids]
    except:
        return JsonResponse({'success': False, 'reason': 'Error in parsing message_ids'})

    Message.objects.filter(id__in=message_ids, recipient=request.user).update(status=MessageStatus.READ)

    return JsonResponse({'success': True})

