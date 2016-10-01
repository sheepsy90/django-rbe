from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, render

# Create your views here.
from django.template import RequestContext

@login_required
def info(request):
    rc = RequestContext(request)
    return render_to_response('developer/info.html', rc)