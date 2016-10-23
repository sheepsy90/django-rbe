from django.conf.urls import url

import skills.views

urlpatterns = [
    url(r'add_tag', skills.views.profile_add_tag, name="profile_add_tag"),
    url(r'del_tag', skills.views.profile_del_tag, name="profile_del_tag"),
    url(r'profile_cloud', skills.views.profile_cloud, name="profile_cloud"),
    url(r'discover', skills.views.discover, name="profile_discover"),
    url(r'details/(?P<phrase_id>\d*)', skills.views.phrase_details, name="phrase_details"),
]