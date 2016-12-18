import random
import itertools

import datetime

from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.views import create_user
from location.models import Location
from messaging.models import Message, MessageStatus
from organizations.models import Organization, OrganizationTag
from organizations.views import create_organization
from profile.models import UserProfile, LanguageSpoken
from skills.models import SlugPhrase, UserSkill


class Command(BaseCommand):
    help = 'Creates an initital state of the system for local development'


    def handle(self, *args, **options):
        User.objects.all().delete()

        usernames = list(itertools.product(['Anne', 'Robert', 'Marie', 'Tove', 'Jens', 'Ines'], ['Larson', 'Nilson', 'Weier', 'Wa', 'Halakkai', 'Czetec']))
        usernames = ["{}.{}".format(e[0], e[1]) for e in usernames]
        usernames.append('sheepy')

        skill_sample_list = ['running', 'flying', 'diving', 'programming', 'dancing', 'cutting video', 'jumping', 'sking', 'eating', 'washing', 'brooming', 'walking']
        sample_languages = dict(LANGUAGES).keys()

        for name in usernames:
            # Create the user
            user = create_user(name, '{}@heleska.de'.format(name), 'aqwsderf')

            # Add a location in some cases
            if random.random() > 0.2:
                long = str(random.randint(-900, 900) / 10.0)
                lang = str(random.randint(-1800, 1800) / 10.0)

                l = Location(user=user, longitude=long, latitude=lang, position_updated=datetime.datetime.today())
                l.save()

            # Add some skills
            num_skills = random.randint(0, len(skill_sample_list))
            for value in random.sample(skill_sample_list, num_skills):
                slug, created = SlugPhrase.objects.get_or_create(value=value)
                UserSkill(user=user, slug=slug, level=random.randint(1, 5)).save()

            # Add some languages
            num_languages = random.randint(0, len(sample_languages))
            for value in random.sample(sample_languages, num_languages):
                LanguageSpoken(user=user, language=value).save()

        # Make my user superuser to access admin and so on
        u = User.objects.get(username='sheepy')
        u.is_superuser = True
        u.is_staff = True
        u.status = True
        u.save()

        # Add some messages
        all_profiles = User.objects.all()

        num_messages = 50
        bodies = ["Soem body", "Another body", "1 2 3 4", "Giraffen sind cool"]

        for idx in range(num_messages):
            u1, u2 = random.sample(all_profiles, 2)

            m = Message.create_message(u1, u2, random.choice(bodies), silent=True)
            m.sent_time = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30),
                                                                       minutes=random.randint(0, 60))
            m.save()

            if random.random() > 0.9:
                m.status = MessageStatus.READ

            if random.random() > 0.9:
                m.status = MessageStatus.DELETED

            m.save()

        organization_names = [
            ('The Auravana Project(TAP)', 'http://www.auravana.com', ['community', 'systems', 'scientific',
                                                                        'critical', 'no_money', 'open_source']),
            ('Buckminster Fuller Institute', 'http://www.bfi.org', ['systems', 'scientific'])
        ]

        for element in organization_names:
            ozt = [OrganizationTag.objects.get_or_create(value=e)[0] for e in element[2]]

            org = create_organization(name=element[0], website_url=element[1])
            org.enabled = True
            for e in ozt:
                org.tags.add(e)

            org.save()

        self.stdout.write(self.style.SUCCESS('Successfully create a bunch of users!'))