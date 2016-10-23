from django.conf.urls import include, url
from django.contrib import admin

import core.views
import core.urls

import location.urls
import messaging.urls
import public.urls
import profile.urls
import skills.urls

import public.views

urlpatterns = [
    # The admin urls and the standard index page url
    url(r'^$', core.views.login, name='index'),
    url(r'^faq$', public.views.faq, name='faq'),
    url(r'^admin/', include(admin.site.urls)),

    # The URLs for the specific area
    url(r'^core/', include(core.urls)),
    url(r'^location/', include(location.urls)),
    url(r'^public/', include(public.urls)),
    url(r'^profile/', include(profile.urls)),
    url(r'^skills/', include(skills.urls)),
    url(r'^messaging/', include(messaging.urls)),

    # The openid/oauth2 provider urls
    url(r'^', include('oidc_provider.urls', namespace='oidc_provider')),
]
