
import associated.views
import associated.api

from django.conf.urls import url

urlpatterns = [
     url(r'overview/$',  associated.views.overview, name='associated_overview'),
     url(r'associated_service_info/$',  associated.views.associated_service_info, name='associated_service_info'),
     url(r'associated_service_revoke/(?P<assoc_id>\d*)$',  associated.views.associated_service_revoke, name='associated_service_revoke'),

     url(r'api/simple_sendout$',  associated.api.simple_sendout, name='api_simple_sendout'),
]
