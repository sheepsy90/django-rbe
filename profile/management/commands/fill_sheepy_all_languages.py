from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from library.log import rbe_logger
from library.mail.ProfileCompletionEmail import ProfileCompletionEmail
from location.models import Location
from profile.models import UserProfile, LanguageSpoken


class Command(BaseCommand):
    help = 'Send out profile fill reminder emails to people who dont have an about me or location'


    def handle(self, *args, **options):
        user = User.objects.get(username='sheepy')

        for lang in dict(LANGUAGES).keys():
            LanguageSpoken.objects.get_or_create(user=user, language=lang)