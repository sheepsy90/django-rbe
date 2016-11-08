from geopy.distance import vincenty

from location.models import DistanceCacheEntry

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Refreshes the distances between people in a stupid an simple way that is just a recalculation'

    def handle(self, *args, **options):
        closest_k = options.get('closest_k', 10)

        all_locations = User.objects.exclude(location=None)
        number_distances = 0
        for user_source in all_locations:
            closest_ten = []
            for user_target in all_locations:
                if user_source != user_target:
                    number_distances += 1
                    location_a = (user_source.location.longitude, user_source.location.latitude)
                    location_b = (user_target.location.longitude, user_target.location.latitude)
                    distance_meters = vincenty(location_a, location_b).kilometers

                    closest_ten.append((distance_meters, user_target))
                    closest_ten = sorted(closest_ten, key=lambda x: x[0])[0:closest_k]

            # Create the objects
            DistanceCacheEntry.objects.filter(user_source=user_source).delete()
            obj_lst = [DistanceCacheEntry(user_source=user_source, distance_to=e[1], value=e[0]) for e in closest_ten]
            DistanceCacheEntry.objects.bulk_create(obj_lst)
