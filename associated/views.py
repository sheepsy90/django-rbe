from __future__ import unicode_literals

import re
import requests

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from associated.models import AssociatedService


@login_required
def overview(request):
    rc = RequestContext(request)
    rc['assoc_services'] = AssociatedService.objects.filter(enabled=True)
    return render_to_response('associated/overview.html', rc)


@login_required
def associated_service_info(request):
    if not request.method == 'POST':
        return JsonResponse({'success': False, 'reason': 'Not a post request'})

    assoc_sid = request.POST.get('assoc_sid')

    if not assoc_sid:
        return JsonResponse({'success': False, 'reason': 'Requires valid assoc_sid'})

    try:
        assoc_service = AssociatedService.objects.get(id=assoc_sid)
        if not assoc_service.enabled:
            return JsonResponse({'success': False, 'reason': 'Requires valid assoc_sid'})
    except AssociatedService.DoesNotExist:
        return JsonResponse({'success': False, 'reason': 'AssociatedService does not exists'})

    try:
        response = requests.get("{}/meta".format(assoc_service.client.website_url))
        if response.status_code != 200:
            return JsonResponse({'success': False, 'reason': 'Could not retrieve service information'})
        else:
            parameters = response.json()
            users = parameters.get('users', None)
            assert re.match(r'[0-9]+', str(users))

            return JsonResponse({'success': True, 'users': users})
    except:
        return JsonResponse({'success': False, 'reason': 'Could not retrieve service information'})
