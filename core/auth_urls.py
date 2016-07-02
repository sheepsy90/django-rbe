import core.auth_views

from django.conf.urls import patterns, url


urlpatterns = [
     url(r'login/$',  core.auth_views.login, name='login'),
     url(r'logout/$', core.auth_views.logout, name='logout'),
     url(r'register/(?P<registration_key>[\w]*)$', core.auth_views.register, name='register'),
     url(r'reset/$', core.auth_views.reset, name='password_reset'),
     url(r'chpw/(?P<reset_key>[\w]*)$', core.auth_views.chpw, name='chpw'),
     url(r'change_password/$', core.auth_views.change_password, name='change_password'),
]