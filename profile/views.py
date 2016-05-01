from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


# Create your views here.
from django.template import RequestContext


@login_required
def example(request):
    rc = RequestContext(request)
    return render_to_response('example.html', rc)
