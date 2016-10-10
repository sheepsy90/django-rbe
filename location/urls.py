from django.conf.urls import patterns, url

import location.views as loc_views

urlpatterns = [
    url(r'update_location', loc_views.update_location, name="update_location"),
    url(r'clear_location', loc_views.clear_location, name="clear_location"),
    url(r'world_map', loc_views.world_map, name="world_map")
]