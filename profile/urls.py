from django.conf.urls import patterns, url

import profile.views

urlpatterns = patterns('',
     url(r'user/(?P<user_id>\d+)$', profile.views.profile),
     url(r'confirm/(?P<user_id>\d+)$', profile.views.confirm),
     url(r'overview$', profile.views.overview, name="profile-overview"),
     url(r'not_confirmed$', profile.views.not_confirmed, name="profile-not-confirmed"),
)