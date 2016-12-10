import uuid

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from core.models import EmailVerification
from library.mail.SendgridEmailClient import SendgridEmailClient
from library.mail.VerifyMail import VerifyMail


class Command(BaseCommand):
    help = "Sends out an email to everyone who doesn't have a verification yet"

    def handle(self, *args, **options):

        users = User.objects.all()

        for user in users:

            if hasattr(user, 'emailverification') and user.emailverification.confirmed:
                pass
            else:
                ev, created = EmailVerification.objects.get_or_create(user=user)
                if created:
                    ev.key = uuid.uuid4().hex
                    ev.save()

                # Send email
                sec = SendgridEmailClient()
                email = VerifyMail(ev)
                sec.send_mail(email)
                self.stdout.write(self.style.SUCCESS('Sending email to {}!'.format(user.email)))

