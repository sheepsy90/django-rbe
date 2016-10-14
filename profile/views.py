import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render_to_response, render


# Create your views here.
from django.template import RequestContext

from profile.forms import InviteForm
from profile.models import InvitationKey, UserProfile


@login_required
def profile(request, user_id):
    # TODO differe between foreign and other profile in waht is given to the tempalte in the first palce
    if user_id:
        uf = User.objects.filter(id=user_id)
        if uf.exists():
            uf = uf.first()
        else:
            return 404
    else:
        uf = request.user

    rc = RequestContext(request)
    p = UserProfile.objects.get(user=uf)
    rc['profile'] = p
    rc['invited_users'] = UserProfile.objects.filter(invited_by=uf)
    rc['invitation_keys'] = InvitationKey.objects.filter(user=request.user)
    return render_to_response('profile.html', rc)


@login_required
def overview(request):
    rc = RequestContext(request)
    rc['profiles'] = UserProfile.objects.all()
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
            #TODO - restrict double invites across the whole network
            registration_key = form.save(commit=False)
            registration_key.user = request.user
            registration_key.key = str(uuid.uuid4()).replace('-', '')
            registration_key.save()

            if settings.CLOSED_NETWORK_INVITE_SEND:
                send_invite_email(request.user, registration_key.key, registration_key.email)

            return render(request, 'invite.html', {})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = InviteForm()

    return render(request, 'invite.html', {'form': form})


@login_required
def revoke(request, revoke_id):
    rk = InvitationKey.objects.filter(id=revoke_id, user=request.user)
    rk.delete()
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))


