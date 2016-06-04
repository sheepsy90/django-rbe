from django.conf.urls import patterns, include, url
from django.contrib import admin

import core.auth_views

import core.auth_urls
import core.profile_urls

urlpatterns = [
    # Examples:
    url(r'^$', core.auth_views.login, name='index'),
    url(r'^admin/', include(admin.site.urls)),

    #url(r'^inventory/', include('inventory.urls')),
    url(r'^core/', include(core.auth_urls)),
    url(r'^profile/', include(core.profile_urls))
]
