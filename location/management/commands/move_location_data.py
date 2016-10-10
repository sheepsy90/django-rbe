from core.models import Profile
from django.core.management.base import BaseCommand

from location.models import Location


class Command(BaseCommand):
    help = 'Moves the location storage from the old model to the new model'

    def handle(self, *args, **options):

        profiles = Profile.objects.all()

        for profile in profiles:
            l = Location(user=profile.user, latitude=profile.latitude, longitude=profile.longitude, position_updated=profile.position_updated)
            l.save()

        self.stdout.write(self.style.SUCCESS('Successfully copied over location data to new model!'))