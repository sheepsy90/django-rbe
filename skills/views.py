import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from library.log import rbe_logger
from skills.models import SlugPhrase, UserSkill
from skills.view_obj import CapabilityBreakdown


@login_required
def discover(request):
    try:
        rc = RequestContext(request)
        rc['all_objects'] = sorted(SlugPhrase.objects.all().annotate(object_count=Count('userskill')),
                                   key=lambda x: -x.object_count)
        return render_to_response('discover.html', rc)
    except Exception as e:
        rbe_logger.exception(e)
        return HttpResponseRedirect(reverse('error_page'))


@login_required
def phrase_details(request, phrase_id):
    rc = RequestContext(request)

    try:
        sp = SlugPhrase.objects.get(id=phrase_id)
        dist = [UserSkill.objects.filter(slug=sp, level=i).count() for i in range(1, 6)]

        rc['capability'] = CapabilityBreakdown(distribution=dist)
        rc['slug_phrase'] = sp
        rc['user_skill_lst'] = UserSkill.objects.filter(slug=sp).order_by('-level')

    except SlugPhrase.DoesNotExist:
        rbe_logger.info("Accesign a slug that doesn't exists {}".format(phrase_id))

    return render_to_response('phrase_details.html', rc)


@login_required
def create_skill(request):
    skill_name = request.POST.get('skill_name')
    level = request.POST.get('level')

    try:
        level = int(level)
        assert 1 <= level <= 5
    except:
        return JsonResponse({'success': False, 'reason': "Level not given or not in range!"})

    if not skill_name:
        return JsonResponse({'success': False, 'reason': "Skill name not given!"})

    if len(skill_name) > 50:
        return JsonResponse({'success': False, 'reason': "Skill to long! Max 50 characters!"})

    skill_name = skill_name.lower()
    skill_name = skill_name.replace(' ', '_')
    skill_name = skill_name.strip()
    sp, created = SlugPhrase.objects.get_or_create(value=skill_name)

    try:
        us = UserSkill.objects.get(slug=sp, user=request.user)
        return JsonResponse({'success': False, 'reason': "User skill already exists!"})
    except UserSkill.DoesNotExist:
        us = UserSkill(slug=sp, user=request.user, level=level)
        us.save()
        return JsonResponse({'success': True, 'new_level': level, 'skill_id': sp.id})


@login_required
def up_skill_level(request):
    skill_id = request.POST.get('skill_id')

    try:
        sp = UserSkill.objects.get(slug__id=skill_id, user=request.user)
        sp.level = min(5, sp.level+1)
        sp.latest_change = datetime.datetime.now()
        sp.save()
        return JsonResponse({'success': True, 'new_level': sp.level})
    except UserSkill.DoesNotExist:
        return JsonResponse({'success': False, 'reason': "Could not find user skill!"})
    except Exception as e:
        rbe_logger.exception(e)
        return JsonResponse({'success': False, 'reason': "Some error occurred!"})


@login_required
def down_skill_level(request):
    skill_id = request.POST.get('skill_id')

    try:
        sp = UserSkill.objects.get(slug__id=skill_id, user=request.user)
        sp.level = max(1, sp.level-1)
        sp.latest_change = datetime.datetime.now()
        sp.save()
        return JsonResponse({'success': True, 'new_level': sp.level})
    except UserSkill.DoesNotExist:
        return JsonResponse({'success': False, 'reason': "Could not find user skill!"})
    except Exception as e:
        rbe_logger.exception(e)
        return JsonResponse({'success': False, 'reason': "Some error occurred!"})


@login_required
def delete_skill(request):
    skill_id = request.POST.get('skill_id')

    try:
        sp = UserSkill.objects.get(slug__id=skill_id, user=request.user)
        sp.delete()
        return JsonResponse({'success': True})
    except UserSkill.DoesNotExist:
        return JsonResponse({'success': True})
    except Exception as e:
        rbe_logger.exception(e)
        return JsonResponse({'success': False, 'reason': "Some error occurred!"})

@login_required
def change_skills(request):
    rc = RequestContext(request)
    try:
        user_skill_qs = UserSkill.objects.filter(user=request.user).order_by('-level')
        rc['user_skill_qs'] = user_skill_qs
    except UserSkill.DoesNotExist:
        rbe_logger.info("Access request to change user skills with profile not found!")

    return render_to_response('change_user_skills.html', rc)