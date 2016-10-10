import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render

from django.core.mail import send_mail


# Create your views here.
from django.template import RequestContext
from django.conf import settings

from profile.forms import InviteForm
from profile.models import Profile, RegistrationKey


@login_required
def profile(request, user_id):
    uf = User.objects.filter(id=user_id)

    if uf.exists():
        rc = RequestContext(request)
        p = Profile.objects.get(user=uf.first())
        rc['profile'] = p
        rc['invited_users'] = Profile.objects.filter(invited_by=uf.first())
        rc['registration_keys'] = RegistrationKey.objects.filter(user=request.user)
        return render_to_response('profile/profile.html', rc)
    else:
        return 404


@login_required
def overview(request):
    rc = RequestContext(request)
    rc['profiles'] = Profile.objects.all()
    return render_to_response('profile/overview.html', rc)


@login_required
def aboutme(request):
    new_about_me = request.POST.get('new_about_me')

    if len(new_about_me) > 3000:
        return JsonResponse({'success': False, 'reason': "Sorry! Not more than 3000 characters allowed!"})

    prof = Profile.objects.get(user=request.user)
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

    prof = Profile.objects.get(user=request.user)
    prof.avatar_link = static_path_part
    prof.save()

    return JsonResponse({'success': True, 'path': static_path_part})


def send_invite_email(user, key, email):
    send_mail(
        '[RBE Network] Invite',
        '''
            Hey,

            this is an invite to the RBE Network from {}.

            If you did not expect this email please just discard it, it was probably a typo.

            Otherwise you can get to the registration page by following the link to:
             https://rbe.heleska.de/core/register/{}

            Kind regards,
            RBE Network
        '''.format(user.username, key),
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=True,
    )


@login_required
def invite(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = InviteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            registration_key = form.save(commit=False)
            registration_key.user = request.user
            registration_key.key = str(uuid.uuid4()).replace('-', '')
            registration_key.save()

            if settings.CLOSED_NETWORK_INVITE_SEND:
                send_invite_email(request.user, registration_key.key, registration_key.email)

            return HttpResponseRedirect(settings.AFTER_LOGIN_PAGE + str(request.user.id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InviteForm()

    return render(request, 'profile/invite.html', {'form': form})


@login_required
def revoke(request, revoke_id):
    rk = RegistrationKey.objects.filter(id=revoke_id, user=request.user)
    rk.delete()
    return HttpResponseRedirect(settings.AFTER_LOGIN_PAGE + str(request.user.id))
