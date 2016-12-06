from __future__ import unicode_literals

import mock
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from library.mail.NewsletterEmail import NewsletterMail
from library.mail.SendgridEmailClient import SendgridEmailClient


class Command(BaseCommand):
    help = 'Send out an email to a specific set of users.'

    def add_arguments(self, parser):
        parser.add_argument('body_path', type=str)
        parser.add_argument('test_email', type=str)

    def handle(self, *args, **options):
        assert 'body_path' in options, "Need to have a file path to the body"
        assert 'test_email' in options, "Need to have a test_email"

        body_path = options['body_path']
        test_email = options['test_email']
        query_set = User.objects.all()

        with open(body_path, 'r') as f:
            body_content = f.read()

        self.stdout.write(self.style.SUCCESS('User query set has {} user.'.format(query_set.count())))

        user_mock = mock.MagicMock(spec=User)
        user_mock.email = test_email
        user_mock.username = "ShowCaseUser"

        nlm_preview = NewsletterMail(user_mock, body_content)
        sec = SendgridEmailClient()

        sec.send_mail(nlm_preview, overwrite_to=test_email)

        result = raw_input("Send out preview email to {} - do you want to send to all users? [y/N]:".format(test_email))

        if result == 'y':
            self.stdout.write(self.style.SUCCESS('Sending all emails...'))
            for user in query_set:
                nlm = NewsletterMail(user, body_content)
                sec.send_mail(nlm)
            self.stdout.write(self.style.SUCCESS('Done.'))
        else:
            self.stdout.write(self.style.SUCCESS('User abort! Not sending emails!'))


