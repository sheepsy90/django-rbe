
import associated.views

from django.conf.urls import url

urlpatterns = [
     url(r'overview/$',  associated.views.overview, name='associated_overview'),
     url(r'associated_service_info/$',  associated.views.associated_service_info, name='associated_service_info'),
]
