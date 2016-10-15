import datetime
import uuid

from django.core.urlresolvers import reverse

from core.forms import RegistrationForm, LoginForm, PasswordChangeForm, PasswordResetRequest, PasswordReset
from core.models import PasswordResetKey
import django.contrib.auth as djauth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.mail import send_mail
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django_rbe.settings import LOGIN_URL, DEFAULT_FROM_EMAIL

from django.conf import settings

from profile.models import InvitationKey, UserProfile


def login(request):
    next_redirect = request.GET.get('next')

    if request.user.is_authenticated():
        if not next_redirect:
            return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))
        else:
            return HttpResponseRedirect(next_redirect)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = djauth.authenticate(username=username, password=password)

            if user is None:
                errors = form._errors.setdefault(NON_FIELD_ERRORS, ErrorList())
                errors.append(u"Could not authenticate you.")

            else:
                djauth.login(request, user)
                next_redirect = request.POST.get('next')
                if not next_redirect:
                    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))
                else:
                    return HttpResponseRedirect(next_redirect)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form, 'next': next_redirect})


@login_required
def logout(request):
    rc = RequestContext(request)
    djauth.logout(request)
    return HttpResponseRedirect(LOGIN_URL, rc)


def register_info(request):
    rc = RequestContext(request)
    return render_to_response('auth/register_info.html', rc)

def register(request, registration_key):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            registration_key = form.cleaned_data.get('registration_key')

            u = User.objects.create_user(username=username, email=email, password=password)
            user = djauth.authenticate(username=username, password=password)

            if settings.CLOSED_NETWORK:
                rk = InvitationKey.objects.get(key=registration_key)
                p = UserProfile(user=u, invited_by=rk.user)
                p.save()
                rk.delete()
            else:
                p = UserProfile(user=u, invited_by=None)
                p.save()

            # TODO send initial welcome emssage

            djauth.login(request, user)

            return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm(initial={'registration_key': registration_key})

    return render(request, 'auth/register.html', {'form': form, 'closed_network': settings.CLOSED_NETWORK})


def reset(request):
    if request.POST:
        email = request.POST.get('email')

        form = PasswordResetRequest(request.POST)

        if not form.is_valid():
            return render(request, 'auth/reset_password.html', {'form': form})

        u = User.objects.filter(email=email)

        # Check if a user with this email exists and if so send an email
        # If not show also the suggest page so emails cannot be guessed
        if u.exists():
            prk = PasswordResetKey.objects.filter(valid_until__lte=datetime.datetime.now())
            prk.delete()

            reset_key = str(uuid.uuid4()).replace('-', '')
            valid_until = datetime.datetime.now() + datetime.timedelta(hours=2)
            pwrk = PasswordResetKey(user=u.first(), key=reset_key, valid_until=valid_until)
            pwrk.save()

            send_mail('[RBE Network] Password reset',
                      '''Hey {},

                        this is an password reset to the RBE Network.

                        If you did not expect this email please just discard it, it was probably a typo.

                        Otherwise you can get to the password reset page following the link to:
                        https://rbe.heleska.de/core/chpw/{}

                        The link will be valid until: {}

                        Kind regards,
                        RBE Network'''.format(u.first().username, reset_key, valid_until.isoformat()), DEFAULT_FROM_EMAIL, [email], fail_silently=True)


        return render_to_response('auth/reset_password_email_send.html', {'email': email})
    else:
        return render(request, 'auth/reset_password.html', {'form': PasswordResetRequest()})


def suggest_close_by(request):
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')

    # TODO - Change to real data not to my personal fake one

    person = {
        'name': 'Robert Kessler',
        'fb': 'https://www.facebook.com/profile.php?id=100010614489059'
    }

    return JsonResponse({'success': True, 'person': person})

@login_required
def change_password(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordChangeForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')

            user = djauth.authenticate(username=request.user.username, password=old_password)

            if user == request.user:
                request.user.set_password(new_password)
                return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.id}))
            else:
                errors = form._errors.setdefault("old_password", ErrorList())
                errors.append(u"The current password was not correct!")


    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordChangeForm()

    return render(request, 'auth/change_password.html', {'form': form})


def chpw(request, reset_key):
    if request.method == 'POST':
        form = PasswordReset(request.POST)
        # check whether it's valid:
        if form.is_valid():
            key = form.cleaned_data.get('key')
            new_password = form.cleaned_data.get('new_password')
            resettable = PasswordResetKey.objects.filter(key=key)

            if resettable.count() == 1:
                user = resettable.first().user
                user.set_password(new_password)
                user.save()
                resettable.delete()
                return render(request, 'auth/chpw.html', {'form': form, 'success': True})
    else:
        resettable = PasswordResetKey.objects.filter(key=reset_key, valid_until__gte=datetime.datetime.now())
        form = None
        if resettable.exists():
            form = PasswordReset(initial={'key': reset_key})

    return render(request, 'auth/chpw.html', {'form': form})

