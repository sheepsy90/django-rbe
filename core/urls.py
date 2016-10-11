import core.views

from django.conf.urls import url

urlpatterns = [
     url(r'login/$',  core.views.login, name='login'),
     url(r'logout/$', core.views.logout, name='logout'),
     url(r'register/(?P<registration_key>[\w]*)$', core.views.register, name='register'),
     url(r'register_info$', core.views.register_info, name='register_info'),
     url(r'reset/$', core.views.reset, name='password_reset'),
     url(r'chpw/(?P<reset_key>[\w]*)$', core.views.chpw, name='chpw'),
     url(r'change_password/$', core.views.change_password, name='change_password'),
     url(r'suggest_close_by/$', core.views.suggest_close_by, name='suggest_close_by'),
]
