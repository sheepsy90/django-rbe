from django.conf.urls import patterns, url

import profile.views

urlpatterns = [
    url(r'overview$', profile.views.overview, name="profile-overview"),
    url(r'aboutme', profile.views.aboutme, name="profile_about_me_change"),
    url(r'avatar_upload', profile.views.avatar_upload, name="profile_avatar_upload"),
    url(r'avatar_delete', profile.views.avatar_delete, name="profile_avatar_delete"),
    url(r'user/(?P<user_id>\d*)$', profile.views.profile, name='profile'),
    url(r'language_remove', profile.views.language_remove, name="language_remove"),
    url(r'language_add', profile.views.language_add, name="language_add"),
    url(r'language_overview/(?P<language_code>\w*)', profile.views.language_overview, name="language_overview"),
    url(r'language_chart', profile.views.language_chart, name="language_chart"),

    url(r'change_about', profile.views.change_about, name="change_about"),
    url(r'change_languages', profile.views.change_languages, name="change_languages"),

]