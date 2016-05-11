from core.models import Profile
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Creates a user for testing the system'

    def handle(self, *args, **options):
        u = User.objects.create_superuser('sheepy', 'sheepy@test.de', 'aqwsderf')
        p = Profile(user=u, invited_by=None, is_confirmed=True)
        p.save()

        self.stdout.write(self.style.SUCCESS('Successfully create test user!'))