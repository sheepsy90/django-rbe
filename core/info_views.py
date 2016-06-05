from django.shortcuts import render_to_response
from django.template.context import RequestContext


def general(request):
    rc = RequestContext(request)
    return render_to_response('info/general.html', rc)