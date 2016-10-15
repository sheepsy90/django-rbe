import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from messaging.models import Message, MessageStatus


class Command(BaseCommand):
    help = 'Create some test messages across users for testing'

    def handle(self, *args, **options):
        all_profiles = User.objects.all()

        subjects = ["Hey", "whats up?", "Something", "Another"]
        bodies = ["Soem body", "Another body", "1 2 3 4", "Giraffen sind cool"]

        for idx in range(all_profiles.count()):

            u1, u2 = random.sample(all_profiles, 2)

            m = Message.create_message(u1, u2, random.choice(subjects), random.choice(bodies))

            if random.random() > 0.9:
                m.status = MessageStatus.READ

            if random.random() > 0.9:
                m.status = MessageStatus.DELETED

            m.save()