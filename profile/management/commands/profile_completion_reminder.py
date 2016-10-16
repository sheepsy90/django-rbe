from django.core.mail import send_mail

from django.core.management.base import BaseCommand

from django_rbe.settings import DEFAULT_FROM_EMAIL
from profile.models import UserProfile

""" TODO FIX THIS COMMAND """
class Command(BaseCommand):
    help = 'Make sendouts to everyone who does not filled their profile with a text.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sendout',
            action='store_true',
            dest='sendout',
            default=False,
            help='Really making the sendouts',
        )

    def handle(self, *args, **options):
        all_profiles = UserProfile.objects.all()
        do_sendouts = options['sendout']

        for profile in all_profiles:
            about_me_length = len(profile.about_me_text)

            if about_me_length == 0:
                self.stdout.write(self.style.SUCCESS('User has no about me: {}'.format(profile.user.username)))
                if do_sendouts:
                    send_email_for_about_me(profile.user)

            if profile.tags.count() == 0:
                self.stdout.write(self.style.SUCCESS('User has no tags: {}'.format(profile.user.username)))
                if do_sendouts:
                    send_email_for_tags(profile.user)


def send_email_for_tags(user):
    send_mail(
        '[RBE Network] Profile completion',
        '''
            Hey {},

            this is a friendly reminder to add some tags about your skills/interests to your profile.
            You can easily see your profile at https://rbe.heleska.de/profile/user/{}

            ----

            If you did not expect this email please just discard it, it was probably a typo.

            Kind regards,
            RBE Network
            https://rbe.heleska.de
        '''.format(user.username, user.id),
        DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )

def send_email_for_about_me(user):
    send_mail(
        '[RBE Network] Profile completion',
        '''
            Hey {},

            this is a friendly reminder to add an introducing statement about yourself to your profile.
            You can easily see your profile at https://rbe.heleska.de/profile/user/{}

            ----

            If you did not expect this email please just discard it, it was probably a typo.

            Kind regards,
            RBE Network
            https://rbe.heleska.de
        '''.format(user.username, user.id),
        DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )