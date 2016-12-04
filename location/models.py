from __future__ import  unicode_literals

import datetime
import random

from django.contrib.auth.models import User
from django.db import models

from location.constants import COUNTRIES

LOCATION_PRECISION = [
    ('rough', 'Rough Location'),
    ('precise', 'Precise Location')
]

class Location(models.Model):

    class Meta:
        db_table = 'geo_location'

    user = models.OneToOneField(User)
    latitude = models.FloatField(blank=True, null=True, help_text="Latitude of the user")
    longitude = models.FloatField(blank=True, null=True, help_text="Longitude of the user")
    position_updated = models.DateTimeField(blank=True, null=True, help_text="The time the location was updated last")
    location_precision = models.CharField(max_length=32, default=LOCATION_PRECISION[1][0], choices=LOCATION_PRECISION,
                                          help_text="How accurate the location should be shown to the outside world.")

    country = models.CharField(max_length=128, default=COUNTRIES[0][0], choices=COUNTRIES,
                               help_text="The country corresponding to the location.")

    location_trace = models.TextField(default='', help_text="The country corresponding to the location.")

    @property
    def display_latitude(self):
        if self.location_precision == LOCATION_PRECISION[0][0]:
            return "{0:.1f}".format(self.latitude)
        else:
            return self.latitude

    @property
    def display_longitude(self):
        if self.location_precision == LOCATION_PRECISION[0][0]:
            return "{0:.1f}".format(self.longitude)
        else:
            return self.longitude


class DistanceCacheEntry(models.Model):
    user_source = models.ForeignKey(User, related_name='user_source')
    distance_to = models.ForeignKey(User, related_name='distance_to')
    value = models.IntegerField()
