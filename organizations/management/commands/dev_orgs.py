import random

import time
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from organizations.models import OrganizationTag, Organization, OrganizationPost
from organizations.views import create_organization

initial_orgs = [
    ['V-radio', 'http://v-radio.org/', ['no-money']],
    ['WikiHouse', 'http://www.wikihouse.cc/', ['architecture']],
    ['World Science U', 'http://www.worldscienceu.com/', ['science', 'educatation']]
]


class Command(BaseCommand):
    help = "creates the initial set of organizations"

    def handle(self, *args, **options):
        Organization.objects.all().delete()

        for element in initial_orgs:
            ozt = [OrganizationTag.objects.get_or_create(value=e)[0] for e in element[2]]

            org = create_organization(name=element[0], website_url=element[1])
            org.enabled = True
            for e in ozt:
                org.tags.add(e)

            org.save()

        u = User.objects.all().first()

        for i in range(15):
            OrganizationPost(organization=random.choice(Organization.objects.all()), content="The post", created=timezone.now(), author=u).save()
            time.sleep(1)