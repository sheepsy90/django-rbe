from django.conf.urls import patterns, url

import inventory.views as iventory_view

urlpatterns = patterns('',
     url(r'overview/$', iventory_view.overview),
     url(r'details/(?P<object_id>[0-9]+)$', iventory_view.details),
)