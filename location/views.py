from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.utils import timezone

from location.forms import LocationDetailsForm
from location.models import Location


@login_required(login_url='/index')
def world_map(request):
    rc = RequestContext(request)
    rc['locations'] = Location.objects.exclude(position_updated=None).exclude(user=request.user)
    return render_to_response('world_map.html', rc)


@login_required(login_url=settings.LOGIN_URL)
def change_location(request):
    try:
        location = Location.objects.get(user=request.user)
    except Location.DoesNotExist:
        location = Location(user=request.user)
        location.save()

    if request.method == 'POST':
        form = LocationDetailsForm(request.POST)

        if form.is_valid():

            if form.has_location:
                long, lat = form.longlat_value
                location.longitude = long
                location.latitude = lat
                location.location_precision = form.cleaned_data['location_precision']
                location.location_trace = form.cleaned_data['location_trace']
                location.country = form.cleaned_data['country']
                location.position_updated = timezone.datetime.now(tz=timezone.get_current_timezone())
                location.save()
            else:
                location.longitude = None
                location.latitude = None
                location.location_trace = ''
                location.country = '-'
                location.position_updated = None
                location.save()

            return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))

    else:
        form = LocationDetailsForm(initial={
            'longitude': location.longitude,
            'latitude': location.latitude,
            'location_precision': location.location_precision,
            'location_trace': location.location_trace,
            'country': location.country
        })

    return render(request, 'location_update.html', {'form': form})