import random
import itertools
from core.models import Profile
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Creates a user for testing the system'

    def handle(self, *args, **options):

        possibilities = list(itertools.product(['Anne', 'Robert', 'Marie', 'Tove', 'Jens', 'Ines', 'Lars', 'Karl'], ['Larson', 'Nilson', 'Weier', 'Mueller', 'Chu-Xi', 'Wa', 'Halakkai', 'Czetec']))
        random.shuffle(possibilities)

        usernames = [e[0] + " " + e[1] for e in possibilities[0:25]]

        users = []
        for name in usernames:
            u = User.objects.create_user(name, '{}@test.de'.format(name.replace(' ', '_')), 'aqwsderf')

            iby = None

            if len(users) > 0 and random.random() > 0.3:
                iby = random.choice(users)

            p = Profile(user=u, invited_by=iby, is_confirmed=True)
            p.save()

            users.append(u)

        self.stdout.write(self.style.SUCCESS('Successfully create a bunch of users!'))