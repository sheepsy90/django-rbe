from django.conf.urls import patterns, url

import core.profile_views as profile_views

urlpatterns = [
    url(r'user/(?P<user_id>\d+)$', profile_views.profile),
    url(r'overview$', profile_views.overview, name="profile-overview"),

    url(r'add_tag', profile_views.profile_add_tag, name="profile_add_tag"),
    url(r'del_tag', profile_views.profile_del_tag, name="profile_del_tag"),
    url(r'profile_cloud', profile_views.profile_cloud, name="profile_cloud"),
    url(r'discover', profile_views.discover, name="profile_discover"),
    url(r'aboutme', profile_views.aboutme, name="profile_about_me_change"),
    url(r'avatar_upload', profile_views.avatar_upload, name="profile_avatar_upload"),
    url(r'invite', profile_views.invite, name="invite"),
    url(r'revoke/(?P<revoke_id>\d+)', profile_views.revoke, name="revoke"),
    url(r'update_location', profile_views.update_location, name="profile_update_location"),
    url(r'clear_location', profile_views.clear_location, name="profile_clear_location"),
    url(r'map', profile_views.map, name="profile_map")
]