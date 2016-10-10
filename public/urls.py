from django.conf.urls import url

import core.info_views as info_views

urlpatterns = [
    url(r'general', info_views.general, name="information")
]