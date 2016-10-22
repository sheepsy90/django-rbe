from django.shortcuts import render_to_response
from django.template import RequestContext


def general(request):
    rc = RequestContext(request)
    return render_to_response('public/general.html', rc)

def developer(request):
    rc = RequestContext(request)
    return render_to_response('public/developer.html', rc)

def faq(request):
    rc = RequestContext(request)
    return render_to_response('public/faq.html', rc)



""" parking this here for the moment
@require_http_methods(['GET'])
@protected_resource_view(['location'])
def protected_api(request, *args, **kwargs):
    dic = {
        'protected': 'information',
        'username': kwargs['token'].user.username
    }

    return JsonResponse(dic, status=200)
"""