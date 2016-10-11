from django.conf.urls import url

import core.profile_views as profile_views

urlpatterns = [

    url(r'add_tag', profile_views.profile_add_tag, name="profile_add_tag"),
    url(r'del_tag', profile_views.profile_del_tag, name="profile_del_tag"),
    url(r'profile_cloud', profile_views.profile_cloud, name="profile_cloud"),
    url(r'discover', profile_views.discover, name="profile_discover"),

]