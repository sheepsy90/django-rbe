from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


# Create your views here.
from django.template import RequestContext

from inventory.models import Object

#@login_required
def overview(request):
    rc = RequestContext(request)
    objects = Object.objects.all()
    rc['objects'] = objects
    return render_to_response('inventory_overview.html', rc)