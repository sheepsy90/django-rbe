import random
import itertools
from core.models import Profile, Tag
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Creates a user for testing the system'

    def handle(self, *args, **options):

        possibilities = list(itertools.product(['Anne', 'Robert', 'Marie', 'Tove', 'Jens', 'Ines', 'Lars', 'Karl'], ['Larson', 'Nilson', 'Weier', 'Mueller', 'Chu-Xi', 'Wa', 'Halakkai', 'Czetec']))
        random.shuffle(possibilities)

        tags = ['banana', 'apple', 'fruit', 'ice', 'green', 'red']
        tags_obj = []
        for t in tags:
            tg = Tag(value=t)
            tg.save()
            tags_obj.append(tg)

        usernames = [e[0] + " " + e[1] for e in possibilities[0:25]]

        users = []
        for name in usernames:
            u = User.objects.create_user(name, '{}@test.de'.format(name.replace(' ', '_')), 'aqwsderf')

            iby = None

            if len(users) > 0 and random.random() > 0.3:
                iby = random.choice(users)

            p = Profile(user=u, invited_by=iby, is_confirmed=True)
            p.save()

            num = random.randint(0, len(tags))
            for e in random.sample(tags_obj, num):
                p.tags.add(e)
            p.save()



            users.append(u)

        self.stdout.write(self.style.SUCCESS('Successfully create a bunch of users!'))