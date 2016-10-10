from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render_to_response, render

# Create your views here.
from django.template import RequestContext
from django.views.decorators.http import require_http_methods
from oidc_provider.lib.utils.oauth2 import protected_resource_view


@login_required
def info(request):
    rc = RequestContext(request)
    return render_to_response('info/developer.html', rc)


@require_http_methods(['GET'])
@protected_resource_view(['location'])
def protected_api(request, *args, **kwargs):


    dic = {
        'protected': 'information',
        'username': kwargs['token'].user.username
    }

    return JsonResponse(dic, status=200)
