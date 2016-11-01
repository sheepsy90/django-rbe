from django.conf.urls import url

import skills.views

urlpatterns = [
    url(r'add_tag', skills.views.profile_add_tag, name="profile_add_tag"),
    url(r'del_tag', skills.views.profile_del_tag, name="profile_del_tag"),
    url(r'profile_cloud', skills.views.profile_cloud, name="profile_cloud"),
    url(r'discover', skills.views.discover, name="profile_discover"),
    url(r'details/(?P<phrase_id>\d*)', skills.views.phrase_details, name="phrase_details"),

    url(r'create_skill$', skills.views.create_skill, name="create_skill"),
    url(r'up_skill_level', skills.views.up_skill_level, name="up_skill_level"),
    url(r'down_skill_level', skills.views.down_skill_level, name="down_skill_level"),
    url(r'delete_skill', skills.views.delete_skill, name="delete_skill"),
]