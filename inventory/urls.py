from django.conf.urls import patterns, url

import inventory

urlpatterns = patterns('',
     url(r'overview/$', 'inventory.views.overview'),
     #url(r'create/$', 'inventory.views.create'),
)