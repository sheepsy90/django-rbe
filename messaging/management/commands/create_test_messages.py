import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from library.mail.AdminMail import AdminMail
from library.mail.GoogleSession import GoogleSession
from messaging.models import Message, MessageStatus


class Command(BaseCommand):
    help = 'Create some test messages across users for testing'

    def handle(self, *args, **options):
        AdminMail(GoogleSession()).send('[RBE Network] Newsletter', 'Some message <br> <b>Blaaa</b>', None)

        # Add some messages
        all_profiles = User.objects.all()

        num_messages = 500
        subjects = [u"Hey", u"whats up?", u"Something", u"Another"]
        bodies = [u"Soem body", u"Another body", u"1 2 3 4", u"Giraffen sind cool"]

        for idx in range(num_messages):
            u1, u2 = random.sample(all_profiles, 2)

            m = Message.create_message(u1, u2, random.choice(subjects), random.choice(bodies), silent=True)

            if random.random() > 0.9:
                m.status = MessageStatus.READ

            if random.random() > 0.9:
                m.status = MessageStatus.DELETED

            m.save()