from urlparse import urlparse
from core.forms import RegistrationForm, LoginForm
from core.models import Profile
import django.contrib.auth as djauth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import NON_FIELD_ERRORS
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, resolve_url
from django.template import RequestContext
from django.utils.decorators import available_attrs
from django.utils.six import wraps
from django_rbe_inventory.settings import AFTER_LOGIN_PAGE, LOGIN_URL

from django.conf import settings


def __user_confirmed(user):
    if settings.CLOSED_NETWORK:
        return Profile.objects.get(user).is_confirmed
    else:
        return True


def user_confirmed(function=None, redirect_field_name='next', login_url=settings.CLOSED_NETWORK_INFO):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    def test(user):
        if not user.is_authenticated():
            return False

        p = Profile.objects.get(user=user)

        return p.is_confirmed

    actual_decorator = user_passes_test(
        test,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )

    if function:
        print function
        return actual_decorator(function)
    return actual_decorator


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(AFTER_LOGIN_PAGE)

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
                return HttpResponseRedirect(AFTER_LOGIN_PAGE)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    rc = RequestContext(request)
    djauth.logout(request)
    return HttpResponseRedirect(LOGIN_URL, rc)


def register(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = RegistrationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            reference_user = form.cleaned_data.get('reference_user')

            u = User.objects.create_user(username=username, email=email, password=password)
            user = djauth.authenticate(username=username, password=password)

            if settings.CLOSED_NETWORK:
                reference_user = User.objects.get(username=reference_user)
                p = Profile(user=u, invited_by=reference_user)
                p.save()
            else:
                p = Profile(user=u, invited_by=None)
                p.save()

            djauth.login(request, user)

            print "Valid"
            return HttpResponseRedirect(AFTER_LOGIN_PAGE)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form, 'closed_network': settings.CLOSED_NETWORK})


def reset(request):
    return HttpResponse('Sorry - feature not available yet!')
