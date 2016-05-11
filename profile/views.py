from core.models import Profile
from core.views import user_confirmed
from django.contrib.auth.models import User
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
