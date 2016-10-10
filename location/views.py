import re
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from location.models import Location, LocationPrecision


@login_required(login_url='/index')
def update_location(request):
    """ This method updates the location of the user """
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    if not longitude or not latitude:
        return JsonResponse({'success': False, 'error': 'Longitude or Latitude not defined'})

    try:
        location = Location.objects.get(user=request.user)
    except Location.DoesNotExist:
        location = Location(user=request.user)
    except Exception:
        return JsonResponse({'success': False, 'error': 'Longitude or Latitude not defined'})

    location.update_location(longitude, latitude)
    return JsonResponse({'success': True})


@login_required(login_url='/index')
def clear_location(request):
    """ This method allows to clear the location """
    try:
        location = Location.objects.get(user=request.user)
        location.clear_location()
        return JsonResponse({'success': True})
    except Location.DoesNotExist:
        location = Location(user=request.user)
        location.save()
        return JsonResponse({'success': True})
    except Exception:
        return JsonResponse({'success': False, 'error': 'Could not find location object'})


@login_required(login_url='/index')
def change_precision(request):
    """ This method allows change the precision of the location based on the user's preference"""
    precision = request.POST.get('precision')

    if not precision:
        return JsonResponse({'success': False, 'error': 'Precision not set'})

    if not re.match(r'[0-9]+', precision):
        return JsonResponse({'success': False, 'error': 'Precision in wrong format'})

    precision = int(precision)

    if precision not in [LocationPrecision.PRECISE, LocationPrecision.ROUGH]:
        return JsonResponse({'success': False, 'error': 'Precision in wrong format'})

    try:
        location = Location.objects.get(user=request.user)
    except Location.DoesNotExist:
        location = Location(user=request.user)
        location.save()
    except Exception:
        return JsonResponse({'success': False, 'error': 'Could not find location object'})

    location.location_precision = precision
    location.save()

    return JsonResponse({'success': True})


@login_required(login_url='/index')
def world_map(request):
    rc = RequestContext(request)
    rc['locations'] = Location.objects.exclude(position_updated=None).exclude(user=request.user)
    return render_to_response('world_map.html', rc)
