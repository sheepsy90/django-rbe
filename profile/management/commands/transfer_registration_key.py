
from core.models import RegistrationKey
from django.core.management.base import BaseCommand

from profile.models import InvitationKey


class Command(BaseCommand):
    help = 'Transfers the registration keys over to the new model.'

    def handle(self, *args, **options):
        registration_keys = RegistrationKey.objects.all()

        for registration_key in registration_keys:
            ik = InvitationKey(user=registration_key.user, key=registration_key.key, email=registration_key.email)
            ik.save()