from django.conf.urls import patterns, include, url
from django.contrib import admin

import core.auth_views

import core.auth_urls
import core.profile_urls
import core.info_urls
import core.developer_urls

urlpatterns = [
    # The admin urls and the standard index page url
    url(r'^$', core.auth_views.login, name='index'),
    url(r'^admin/', include(admin.site.urls)),

    # The URLs for the specific area
    url(r'^core/', include(core.auth_urls)),
    url(r'^profile/', include(core.profile_urls)),
    url(r'^info/', include(core.info_urls)),
    url(r'^developer/', include(core.developer_urls)),

    # The openid/oauth2 provider urls
    url(r'^', include('oidc_provider.urls', namespace='oidc_provider')),
]
