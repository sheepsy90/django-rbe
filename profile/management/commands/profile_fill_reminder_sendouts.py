
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from library.log import rbe_logger
from library.mail.ProfileCompletionEmail import ProfileCompletionEmail
from location.models import Location
from profile.models import UserProfile, LanguageSpoken


class Command(BaseCommand):
    help = 'Send out profile fill reminder emails to people who dont have an about me or location'

    def has_location(self, user):
        try:
            l = Location.objects.get(user=user)
            return l.position_updated is not None
        except Location.DoesNotExist:
            return False

    def handle(self, *args, **options):
        all_users = User.objects.filter(username='sheepy')

        for user in all_users:
            location_missing = not self.has_location(user)
            about_missing = not self.has_about(user)
            languages_missing = not self.has_languages(user)

            if location_missing or about_missing or languages_missing:
                gec = ProfileCompletionEmail()
                gec.send(username=user.username, recipient_list=[user.email], location_missing=location_missing, about_missing=about_missing, languages_missing=languages_missing)
                rbe_logger.info("Sending email to {} for profile fill reminder on Loc:{} / About:{}".format(user.email, location_missing, about_missing))
            else:
                rbe_logger.info("Skipping email {} - already filled profile.".format(user.email))

    def has_about(self, user):
        up = UserProfile.objects.get(user=user)
        return len(up.about_me_text) > 50

    def has_languages(self, user):
        return LanguageSpoken.objects.filter(user=user).count() > 0