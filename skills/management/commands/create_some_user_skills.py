import random

from django.contrib.auth.models import User
from django.core.management import BaseCommand

from skills.models import SlugPhrase, UserSkill

sample_skills = [u'computer_science', u'programming', u'microelectronics', u'electronics', u'django', u'python', u'automation', u'biology']


class Command(BaseCommand):
    help = 'Creates some user skills'

    def handle(self, *args, **options):

        for element in sample_skills:
            sp, created = SlugPhrase.objects.get_or_create(value=element)

            for user in User.objects.all():

                if random.random() > 0.9:
                    UserSkill.objects.get_or_create(user=user, slug=sp, level=random.randint(1,6))

