import core.views
import core.api

from django.conf.urls import url

urlpatterns = [
     url(r'login/$',  core.views.login, name='login'),
     url(r'logout/$', core.views.logout, name='logout'),
     url(r'register/(?P<registration_key>[\w]*)$', core.views.register, name='register'),
     url(r'reset/$', core.views.reset, name='password_reset'),
     url(r'chpw/(?P<reset_key>[\w]*)$', core.views.chpw, name='chpw'),
     url(r'change_password/$', core.views.change_password, name='change_password'),
     url(r'error_page/$', core.views.error_page, name='error_page'),
     url(r'api/identity/$', core.api.identity, name='api_identity'),
]
