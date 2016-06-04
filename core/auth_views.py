from core.forms import RegistrationForm, LoginForm
from core.models import Profile, RegistrationKey
import django.contrib.auth as djauth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django_rbe_inventory.settings import AFTER_LOGIN_PAGE, LOGIN_URL

from django.conf import settings


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(AFTER_LOGIN_PAGE + str(request.user.id))

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
                return HttpResponseRedirect(AFTER_LOGIN_PAGE + str(user.id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'authorizing/login.html', {'form': form})


@login_required
def logout(request):
    rc = RequestContext(request)
    djauth.logout(request)
    return HttpResponseRedirect(LOGIN_URL, rc)


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
                rk = RegistrationKey.objects.get(key=registration_key)
                p = Profile(user=u, invited_by=rk.user)
                p.save()
                rk.delete()
            else:
                p = Profile(user=u, invited_by=None)
                p.save()

            djauth.login(request, user)

            return HttpResponseRedirect(AFTER_LOGIN_PAGE + str(p.user.id))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm(initial={'registration_key': registration_key})

    return render(request, 'authorizing/register.html', {'form': form, 'closed_network': settings.CLOSED_NETWORK})


def reset(request):
    return HttpResponse('Sorry - feature not available yet!')
