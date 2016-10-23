from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from library.log import rbe_logger
from skills.models import SlugPhrase, UserSlugs


@login_required
def profile_add_tag(request):
    value = request.POST.get('value')

    value = value.strip().replace(' ', '_').lower()

    t = SlugPhrase.objects.get_or_create(value=value)[0]
    sp = UserSlugs.objects.get_or_create(user=request.user, slug=t)[0]

    return JsonResponse({'success': True, 'id': sp.id})


@login_required
def profile_del_tag(request):
    tag_id = request.POST.get('tag_id')

    try:
        us = UserSlugs.objects.get(id=tag_id)
        us.delete()
        return JsonResponse({'success': True})

    except UserSlugs.DoesNotExist:
        return JsonResponse({'success': True})

@login_required
def profile_cloud(request):
    chosen_tags = request.POST.get('chosen_tags', None)

    if chosen_tags is None:
        return JsonResponse({'success': False, 'reason': "Something"})

    if chosen_tags == '':
        tags = dict([(e.value, e.object_count) for e in SlugPhrase.objects.all().annotate(object_count=Count('userslugs')) if e.object_count > 0])
    else:
        chosen_tags_lst = chosen_tags.split(',')
        tags = dict([(e.value, e.object_count) for e in SlugPhrase.objects.filter(value__in=chosen_tags_lst).annotate(object_count=Count('userslugs'))])

    sorted_tags = sorted(tags.items(), key=lambda e: -int(e[1]))
    max_tags = sorted_tags[0:5]

    user_slugs = UserSlugs.objects.filter(slug__value__in=[e[0] for e in max_tags]).distinct()

    return JsonResponse({
        'tags': tags,
        'objects': [{'id': us.user.id, 'name': us.user.username} for us in user_slugs]
    })

@login_required
def discover(request):
    try:
        rc = RequestContext(request)
        rc['all_objects'] = sorted(SlugPhrase.objects.all().annotate(object_count=Count('userslugs')), key=lambda x: -x.object_count)
        return render_to_response('discover.html', rc)
    except Exception as e:
        rbe_logger.exception(e)
        return HttpResponseRedirect(reverse('error_page'))


@login_required
def phrase_details(request, phrase_id):
    rc = RequestContext(request)

    try:
        rc['slug_phrase'] = SlugPhrase.objects.get(id=phrase_id)
    except SlugPhrase.DoesNotExist:
        pass

    return render_to_response('phrase_details.html', rc)
