
import associated.views

from django.conf.urls import url

urlpatterns = [
     url(r'overview/$',  associated.views.overview, name='associated_overview'),
]
