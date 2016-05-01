from django.conf.urls import patterns, url

import profile.views

urlpatterns = patterns('',
     url(r'profile/$', profile.views.example, name="profile-example"),
)