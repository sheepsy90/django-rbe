from django.conf.urls import patterns, url

import profile.views

urlpatterns = [
    url(r'overview$', profile.views.overview, name="profile-overview"),
    url(r'aboutme', profile.views.aboutme, name="profile_about_me_change"),
    url(r'avatar_upload', profile.views.avatar_upload, name="profile_avatar_upload"),
    url(r'user/(?P<user_id>\d*)$', profile.views.profile, name='profile'),
    url(r'invite', profile.views.invite, name="invite"),
    url(r'revoke/(?P<revoke_id>\d+)', profile.views.revoke, name="revoke"),

]