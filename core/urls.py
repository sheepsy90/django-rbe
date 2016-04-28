import core.views

from django.conf.urls import patterns, url


urlpatterns = patterns('',
     url(r'login/$',  core.views.login, name='login'),
     url(r'logout/$', core.views.logout, name='logout'),
     url(r'register/$', core.views.register, name='register'),
     url(r'reset/$', core.views.reset, name='password_reset'),
)