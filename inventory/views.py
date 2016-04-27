from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response


# Create your views here.
from django.template import RequestContext

from inventory.models import Object, ObjectLogEntry


@login_required
def overview(request):
    rc = RequestContext(request)
    objects = Object.objects.all()
    rc['objects'] = objects
    return render_to_response('overview.html', rc)

@login_required
def details(request, object_id):
    rc = RequestContext(request)
    objects = Object.objects.filter(unique_identifier=object_id)

    if objects.exists():
        rc['object'] = objects.first()
        rc['log'] = ObjectLogEntry.objects.filter(referenced_object=objects.first())

    return render_to_response('details.html', rc)
