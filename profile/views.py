import uuid

from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render_to_response


# Create your views here.
from django.template import RequestContext

from library.log import rbe_logger
from profile.models import UserProfile, LanguageSpoken


@login_required
def profile(request, user_id):
    rc = RequestContext(request)
    # TODO differe between foreign and other profile in waht is given to the tempalte in the first palce
    if user_id:
        uf = User.objects.filter(id=user_id)
        if uf.exists():
            uf = uf.first()
        else:
            return render_to_response('profile.html', rc)
    else:
        uf = request.user

    p = UserProfile.objects.get(user=uf)
    rc['profile'] = p
    rc['invited_users'] = UserProfile.objects.filter(invited_by=uf)
    return render_to_response('profile.html', rc)


@login_required
def overview(request):
    rc = RequestContext(request)

    user_list = UserProfile.objects.all().order_by('-user__last_login')
    page = request.GET.get('page', 1)

    paginator = Paginator(user_list, 18)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    rc['profiles'] = users
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


def language_overview(request, language_code):
    rc = RequestContext(request)
    return render_to_response('language.html', rc)
