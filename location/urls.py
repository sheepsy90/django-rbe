from django.conf.urls import url

import location.views as loc_views

urlpatterns = [
    url(r'world_map', loc_views.world_map, name="world_map"),
    url(r'change_location', loc_views.change_location, name="change_location")
]