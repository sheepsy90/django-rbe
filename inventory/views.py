from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render_to_response, render


# Create your views here.
from django.template import RequestContext
from inventory.forms import CreateObjectEntryForm

from inventory.models import Object


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

    return render_to_response('details.html', rc)


@login_required
def create(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateObjectEntryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            instance = form.save()
            instance.entered_by = request.user
            instance.save()


            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/inventory/details/{}'.format(instance.unique_identifier))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateObjectEntryForm()

    return render(request, 'enter.html', {'form': form})

@login_required
def cloud(request):

    return JsonResponse({
        'tags': {
            'tool': 2,
            'outdoor': 5,
            'gardening': 2,
            'math': 4,
            'hammer': 1,
            'electronics': 7,
            'art': 3,
            'hard-drive': 3
        },
        'objects': [{
            'object_id': 1
        }]
    })

@login_required
def discover(request):
    rc = RequestContext(request)
    objects = Object.objects.all()
    rc['objects'] = objects
    return render_to_response('discover.html', rc)