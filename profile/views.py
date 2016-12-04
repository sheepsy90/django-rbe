import uuid

from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponseRedirect

from django.shortcuts import render_to_response


# Create your views here.
from django.template import RequestContext

from library.log import rbe_logger
from location.models import DistanceCacheEntry
from profile.constants import LANGUAGE_LEVELS
from profile.forms import ProfileDetailsForm
from profile.models import UserProfile, LanguageSpoken
from skills.models import UserSkill


@login_required(login_url=settings.LOGIN_URL)
def change_about(request):
    rc = RequestContext(request)

    if request.method == 'POST':
        form = ProfileDetailsForm(request.POST)
        if form.is_valid():
            about_me_text = form.cleaned_data['about_me_text']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.save()

            request.user.user.about_me_text = about_me_text
            request.user.user.save()

            return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))

    else:
        form = ProfileDetailsForm(initial={
            'about_me_text': request.user.user.about_me_text,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'profile_email': request.user.email
        })

    rc['form'] = form
    return render_to_response('profile/edit/change_about.html', rc)


@login_required(login_url=settings.LOGIN_URL)
def profile(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        rc = RequestContext(request)
        p = UserProfile.objects.get(user=user)
        rc['my_profile'] = request.user == user
        rc['profile'] = p
        rc['user_skills'] = UserSkill.objects.filter(user=user).order_by('-level')
        rc['closest_people'] = DistanceCacheEntry.objects.filter(user_source=user).order_by('value')
        return render_to_response('profile/profile.html', rc)
    except User.DoesNotExist:
        raise Http404("User not found")


def transform_search_query_to_query_set(search_query, request_user):
    if search_query == '':
        return UserProfile.objects.all()\
            .exclude(user=request_user)\
            .order_by('-user__lastseen__date_time')
    else:
        return UserProfile.objects.all() \
            .exclude(user=request_user) \
            .filter(user__username__icontains=search_query) \
            .order_by('-user__lastseen__date_time')


@login_required
def overview(request):
    rc = RequestContext(request)
    search_query = request.GET.get('search_query', '')

    user_qs = transform_search_query_to_query_set(search_query, request.user)

    page = request.GET.get('page', 1)

    paginator = Paginator(user_qs, 18)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    rc['profiles'] = users
    rc['search_query'] = search_query
    return render_to_response('overview.html', rc)


@login_required
def aboutme(request):
    new_about_me = request.POST.get('new_about_me')

    if len(new_about_me) > 3000:
        return JsonResponse({'success': False, 'reason': "Sorry! Not more than 3000 characters allowed!"})

    prof = UserProfile.objects.get(user=request.user)
    prof.about_me_text = new_about_me
    prof.save()

    return JsonResponse({'success': True})

@login_required
def avatar_delete(request):
    try:
        prof = UserProfile.objects.get(user=request.user)
        prof.avatar_link = ''
        prof.save()
        return JsonResponse({'success': True})
    except UserProfile.DoesNotExist:
        return JsonResponse({'success': False, 'reason': 'UserProfile not found!'})


@login_required
def avatar_upload(request):
    print request.FILES

    file = request.FILES[u'0']
    ending = file.name.split('.')[-1]

    if ending not in ['png', 'jpg', 'jpeg']:
        return JsonResponse({'success': False, 'reason': "Unsupported file ending! allowed is png and jpeg!"})

    random_uuid = str(uuid.uuid4())
    prefix = ''

    if settings.DEBUG:
        prefix = '/core'

    static_path_part = '/static/tmp/img/{}.{}'.format(random_uuid, ending)
    default_storage.save(settings.BASE_DIR + prefix + static_path_part, ContentFile(file.read()))

    prof = UserProfile.objects.get(user=request.user)
    prof.avatar_link = static_path_part
    prof.save()

    return JsonResponse({'success': True, 'path': static_path_part})


@login_required
def language_add(request):
    lang = request.POST.get('lang')

    if not lang or lang not in dict(LANGUAGES):
        return JsonResponse({'success': False, 'reason': "Language code not known!"})

    ls, created = LanguageSpoken.objects.get_or_create(user=request.user, language=lang)

    if created:
        return JsonResponse({'success': True, 'language_display': dict(LANGUAGES)[lang]})
    else:
        return JsonResponse({'success': False, 'reason': 'Language already present'})


@login_required
def language_remove(request):
    """ Removes a language that the suer has registered """
    lang = request.POST.get('lang')

    if not lang or lang not in dict(LANGUAGES):
        return JsonResponse({'success': False, 'reason': "Language code not known!"})

    try:
        ls = LanguageSpoken.objects.get(user=request.user, language=lang)
        ls.delete()
        return JsonResponse({'success': True})
    except LanguageSpoken.DoesNotExist:
        # Language doesn't exists for some reason so we assume we deleted it
        return JsonResponse({'success': True})
    except Exception as e:
        rbe_logger.exception(e)
        return JsonResponse({'success': False, 'reason': "Could not remove language"})

@login_required()
def language_overview(request, language_code):
    rc = RequestContext(request)

    # Return the not with variables filled language page
    if language_code == '' or language_code not in dict(LANGUAGES):
        rc['empty_language_code'] = True
        grouping_count = LanguageSpoken.count_grouping()
        rc['grouping_count'] = grouping_count
        return render_to_response('language.html', rc)
    else:
        rc['language_present'] = {
            'language_display': dict(LANGUAGES)[language_code],
            'language_code': language_code,
        }
        rc['language_spoken_qs'] = LanguageSpoken.objects.filter(language=language_code)
        return render_to_response('language.html', rc)

@login_required()
def change_languages(request):
    rc = RequestContext(request)
    try:
        language_spoken_qs = LanguageSpoken.objects.filter(user=request.user)
        rc['language_levels'] = LANGUAGE_LEVELS
        rc['language_spoken_qs'] = language_spoken_qs
    except UserProfile.DoesNotExist:
        rbe_logger.info("Access request to change language with profile not found!")

    return render_to_response('profile/edit/change_languages.html', rc)

@login_required()
def language_level_change(request):
    lang_code = request.POST.get('lang_code')
    new_value = request.POST.get('new_value')

    if lang_code not in dict(LANGUAGES).keys():
        return JsonResponse({'success': False, 'reason': 'Language code not known!'})

    if new_value not in dict(LANGUAGE_LEVELS).keys():
        return JsonResponse({'success': False, 'reason': 'Language level not known!'})

    try:
        ls = LanguageSpoken.objects.get(user=request.user, language=lang_code)
        ls.level = new_value
        ls.save()
        return JsonResponse({'success': True})
    except LanguageSpoken.DoesNotExist:
        return JsonResponse({'success': False, 'reason': 'Language entry not there!'})
    except Exception:
        return JsonResponse({'success': False, 'reason': 'Something went wrong!'})
