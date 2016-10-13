from core.models import Tag
from django.core.management.base import BaseCommand

from skills.models import SlugPhrase, UserSlugs


class Command(BaseCommand):
    help = 'copies over the tags from core to the new system'

    def handle(self, *args, **options):
        all_tags = Tag.objects.all()

        print all_tags.first().profile_tags.all()

        for tag in all_tags:

            sp = SlugPhrase(value=tag.value)
            sp.save()

            for profile in tag.profile_tags.all():

                us = UserSlugs(user=profile.user, slug=sp)
                us.save()