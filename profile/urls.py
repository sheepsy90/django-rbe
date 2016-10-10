from django.conf.urls import patterns, url

import core.profile_views as profile_views

urlpatterns = [
    url(r'(?P<user_id>\d*)$', profile_views.profile, name='profile'),
    url(r'overview$', profile_views.overview, name="profile-overview"),


    url(r'profile_cloud', profile_views.profile_cloud, name="profile_cloud"),
    url(r'aboutme', profile_views.aboutme, name="profile_about_me_change"),
    url(r'avatar_upload', profile_views.avatar_upload, name="profile_avatar_upload"),
    url(r'invite', profile_views.invite, name="invite"),
    url(r'revoke/(?P<revoke_id>\d+)', profile_views.revoke, name="revoke"),
]