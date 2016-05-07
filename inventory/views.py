from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render_to_response, render

# Create your views here.
from django.template import RequestContext
from inventory.forms import CreateObjectEntryForm

from inventory.models import Object, Tag, DummyEvent, TagModificationLogEvent, SimpleObjectCommentEvent
import library
from library.cloud import CloudFactory


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
        events = objects.first().event_set.all().order_by('-registration_date')[0:15]
        down_casted_events = [getattr(e, e.related_clazz, DummyEvent()) for e in events]
        rc['events'] = down_casted_events

        print down_casted_events

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
    chosen_tags = request.POST.get('chosen_tags', None)

    if chosen_tags is None:
        return JsonResponse({'success': False, 'reason': "Something"})

    if chosen_tags == '':
        tags = dict([(e.value, e.object_count) for e in Tag.objects.all().annotate(object_count=Count('object_tags')) if e.object_count > 0])
    else:
        chosen_tags_lst = chosen_tags.split(',')
        tags = dict([(e.value, e.object_count) for e in Tag.objects.filter(value__in=chosen_tags_lst).annotate(object_count=Count('object_tags'))])

    sorted_tags = sorted(tags.items(), key=lambda e: -int(e[1]))
    max_tags = sorted_tags[0:5]

    objts = Object.objects.filter(tags__value__in=[e[0] for e in max_tags]).distinct()

    return JsonResponse({
        'tags': tags,
        'objects': [{'id': obj.unique_identifier, 'name': obj.title} for obj in objts]
    })


@login_required
def discover(request):
    rc = RequestContext(request)
    objects = Object.objects.all()
    rc['objects'] = objects
    return render_to_response('discover.html', rc)

@login_required
def del_tag(request):
    object_id = request.POST.get('object_id')
    tag_id = request.POST.get('tag_id')

    t = Tag.objects.get(id=tag_id)
    o = Object.objects.get(unique_identifier=object_id)

    o.tags.remove(t)
    o.save()
    tme = TagModificationLogEvent.create(object=o, user=request.user, tag_value=t.value, added=False)

    return JsonResponse({'success': True, 'timeline_html': tme.render()})


@login_required
def submit_comment(request):
    object_id = request.POST.get('object_id')
    comment_text = request.POST.get('comment_text')

    o = Object.objects.get(unique_identifier=object_id)
    so = SimpleObjectCommentEvent.create(object=o, user=request.user, comment_text=comment_text)

    return JsonResponse({'success': True, 'timeline_html': so.render()})


@login_required
def add_tag(request):
    value = request.POST.get('value')
    obj_id = request.POST.get('object_id')

    value = value.strip().replace(' ', '_').lower()

    t = Tag.objects.filter(value=value)
    if t.exists():
        tag_to_add = t.first()
    else:
        tag_to_add = Tag(value=value)
        tag_to_add.save()

    o = Object.objects.filter(unique_identifier=obj_id)

    if o.exists():
        obj = o.first()
        obj.tags.add(tag_to_add)
        obj.save()

        tme = TagModificationLogEvent.create(object=obj, user=request.user, tag_value=value)

        return JsonResponse({'success': True, 'id': tag_to_add.id, 'timeline_html': tme.render()})
    else:
        return JsonResponse({'success': False, 'reason': 'Object does not exist!'})
