import datetime

from django.contrib.auth.models import User
from django.db import models


class LocationPrecision:
    PRECISE = 0
    ROUGH = 1

class Location(models.Model):

    user = models.OneToOneField(User)
    latitude = models.FloatField(blank=True, null=True, help_text="Latitude of the user")
    longitude = models.FloatField(blank=True, null=True, help_text="Longitude of the user")
    position_updated = models.DateTimeField(blank=True, null=True, help_text="The time the location was updated last")
    location_precision = models.IntegerField(default=LocationPrecision.PRECISE, help_text="How accurate the location should be shown to the outside world.")

    def update_location(self, longitude, latitude):
        self.latitude = latitude
        self.longitude = longitude
        self.position_updated = datetime.datetime.now()
        self.save()

    def clear_location(self):
        self.latitude = None
        self.longitude = None
        self.position_updated = None
        self.save()