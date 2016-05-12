from core.models import Profile, Tag
from core.views import user_confirmed
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render_to_response


# Create your views here.
from django.template import RequestContext

@user_confirmed
def profile(request, user_id):
    uf = User.objects.filter(id=user_id)

    if uf.exists():
        rc = RequestContext(request)
        p = Profile.objects.get(user=uf.first())
        rc['profile'] = p
        rc['invited_users'] = Profile.objects.filter(invited_by=uf.first())
        return render_to_response('profile/profile.html', rc)
    else:
        return 404

@user_confirmed
def confirm(request, user_id):
    pass

@user_confirmed
def overview(request):
    rc = RequestContext(request)

    rc['profiles'] = Profile.objects.all()

    return render_to_response('profile/overview.html', rc)


def not_confirmed(request):
    rc = RequestContext(request)
    return render_to_response('profile/not_confirmed.html', rc)


@user_confirmed
def profile_add_tag(request):
    value = request.POST.get('value')

    value = value.strip().replace(' ', '_').lower()

    t = Tag.objects.filter(value=value)
    if t.exists():
        tag_to_add = t.first()
    else:
        tag_to_add = Tag(value=value)
        tag_to_add.save()

    o = Profile.objects.filter(user=request.user)

    if o.exists():
        obj = o.first()
        obj.tags.add(tag_to_add)
        obj.save()

        return JsonResponse({'success': True, 'id': tag_to_add.id})
    else:
        return JsonResponse({'success': False, 'reason': 'Object does not exist!'})


@user_confirmed
def profile_del_tag(request):
    tag_id = request.POST.get('tag_id')

    t = Tag.objects.get(id=tag_id)
    o = Profile.objects.get(user=request.user)

    o.tags.remove(t)
    o.save()

    return JsonResponse({'success': True})


@user_confirmed
def profile_cloud(request):
    chosen_tags = request.POST.get('chosen_tags', None)

    if chosen_tags is None:
        return JsonResponse({'success': False, 'reason': "Something"})

    if chosen_tags == '':
        tags = dict([(e.value, e.object_count) for e in Tag.objects.all().annotate(object_count=Count('profile_tags')) if e.object_count > 0])
    else:
        chosen_tags_lst = chosen_tags.split(',')
        tags = dict([(e.value, e.object_count) for e in Tag.objects.filter(value__in=chosen_tags_lst).annotate(object_count=Count('profile_tags'))])

    sorted_tags = sorted(tags.items(), key=lambda e: -int(e[1]))
    max_tags = sorted_tags[0:5]

    objts = Profile.objects.filter(tags__value__in=[e[0] for e in max_tags]).distinct()

    return JsonResponse({
        'tags': tags,
        'objects': [{'id': obj.user.id, 'name': obj.user.username} for obj in objts]
    })

@user_confirmed
def discover(request):
    rc = RequestContext(request)
    return render_to_response('profile/discover.html', rc)