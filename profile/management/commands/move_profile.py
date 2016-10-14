from core.models import Profile
from django.core.management.base import BaseCommand

from profile.models import UserProfile


class Command(BaseCommand):
    help = 'Make sendouts to everyone who does not filled their profile with a text.'

    def handle(self, *args, **options):
        all_profiles = Profile.objects.all()

        for profile in all_profiles:
            up = UserProfile(user=profile.user, invited_by=profile.invited_by, about_me_text=profile.about_me_text,
                             avatar_link=profile.avatar_link)
            up.save()
