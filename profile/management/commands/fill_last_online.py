from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import LastSeen


class Command(BaseCommand):
    help = 'Initial setup for all users and their last time'

    def handle(self, *args, **options):
        all_users = User.objects.all()
        for user in all_users:
            ls, created = LastSeen.objects.get_or_create(user=user)
            ls.date_time = user.last_login
            ls.save()
