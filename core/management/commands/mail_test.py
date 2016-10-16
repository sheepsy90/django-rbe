from django.core.management.base import BaseCommand
from library.mail.TestEmail import TestEmail


class Command(BaseCommand):
    help = 'Make a test email sendout'

    def handle(self, *args, **options):
        gec = TestEmail()
        gec.send(recipient_list=['8kessler@informatik.uni-hamburg.de'])
