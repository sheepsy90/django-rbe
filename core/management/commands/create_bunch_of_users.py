import random
import itertools

import datetime

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from location.models import Location
from profile.models import UserProfile
from skills.models import SlugPhrase, UserSlugs


class Command(BaseCommand):
    help = 'Creates a user for testing the system'

    def handle(self, *args, **options):

        possibilities = list(itertools.product(['Anne', 'Robert', 'Marie', 'Tove', 'Jens', 'Ines', 'Lars', 'Karl'], ['Larson', 'Nilson', 'Weier', 'Mueller', 'Chu-Xi', 'Wa', 'Halakkai', 'Czetec']))
        random.shuffle(possibilities)

        tags = ['banana', 'apple', 'fruit', 'ice', 'green', 'red']
        tags_obj = []
        for t in tags:
            tg = SlugPhrase.objects.get_or_create(value=t)[0]
            tags_obj.append(tg)

        usernames = [e[0] + " " + e[1] for e in possibilities[0:25]]

        users = []
        for name in usernames:
            u = User.objects.create_user(name, '{}@test.de'.format(name.replace(' ', '_')), 'aqwsderf')

            iby = None

            if len(users) > 0 and random.random() > 0.3:
                iby = random.choice(users)

            p = UserProfile(user=u, invited_by=iby, is_confirmed=True)
            p.about_me_text = "Some about me"
            p.save()

            long = str(random.randint(-900, 900) / 10.0)
            lang = str(random.randint(-1800, 1800) / 10.0)

            l = Location(user=u, longitude=long, latitude=lang, position_updated=datetime.datetime.today())
            l.save()

            num = random.randint(0, len(tags))
            for e in random.sample(tags_obj, num):
                UserSlugs(user=u, slug=e).save()

            users.append(u)

        self.stdout.write(self.style.SUCCESS('Successfully create a bunch of users!'))