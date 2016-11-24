from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from oidc_provider.models import Client

from associated.models import AssociatedService


@login_required
def overview(request):
    rc = RequestContext(request)
    rc['assoc_services'] = AssociatedService.objects.filter(enabled=True)
    return render_to_response('associated/overview.html', rc)

