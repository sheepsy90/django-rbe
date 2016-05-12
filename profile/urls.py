from django.conf.urls import patterns, url

import profile.views

urlpatterns = patterns('',
     url(r'user/(?P<user_id>\d+)$', profile.views.profile),
     url(r'confirm/(?P<user_id>\d+)$', profile.views.confirm),
     url(r'overview$', profile.views.overview, name="profile-overview"),
     url(r'not_confirmed$', profile.views.not_confirmed, name="profile-not-confirmed"),

     url(r'add_tag', profile.views.profile_add_tag, name="profile_add_tag"),
     url(r'del_tag', profile.views.profile_del_tag, name="profile_del_tag"),
     url(r'profile_cloud', profile.views.profile_cloud, name="profile_cloud"),
     url(r'discover', profile.views.discover, name="profile_discover"),
)