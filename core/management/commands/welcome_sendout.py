from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from library.mail.WelcomeMail import WelcomeMail


class Command(BaseCommand):
    help = 'Make a welcome sendout to everyone who is already registered so that they get the email as well'

    def handle(self, *args, **options):
        uqs = User.objects.all()
        for element in uqs:
            gec = WelcomeMail()
            gec.send(username=element.username, recipient_list=['rbe.heleska@gmail.com'])
