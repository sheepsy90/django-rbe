from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from library.mail.AdminMail import AdminMail
from library.mail.GoogleSession import GoogleSession


class Command(BaseCommand):
    help = 'Send out an email to a specific set of users.'

    def add_arguments(self, parser):
        parser.add_argument('body_path', type=str)
        parser.add_argument('subject', type=str)
        parser.add_argument('test_email', type=str)

    def handle(self, *args, **options):
        print args
        print options

        assert 'body_path' in options, "Need to have a file path to the body"
        assert 'subject' in options, "Need to have a subject"
        assert 'test_email' in options, "Need to have a test_email"

        subject = options['subject']
        body_path = options['body_path']
        test_email = options['test_email']
        query_set = User.objects.all()

        with open(body_path, 'r') as f:
            body_content = f.read()

        self.stdout.write(self.style.SUCCESS('User query set has {} user.'.format(query_set.count())))

        google_session = GoogleSession()

        admin_mail = AdminMail(google_session)
        admin_mail.send("{} // Preview".format(subject), body_content, [('RecipientName', test_email)])

        result = raw_input("Send out preview email to {} - do you want to send to all users? [y/N]:".format(test_email))

        if result == 'y':
            self.stdout.write(self.style.SUCCESS('Sending all emails...'))
            admin_mail = AdminMail(google_session)
            admin_mail.send(subject, body_content, query_set.values_list('username', 'email'))
            self.stdout.write(self.style.SUCCESS('Done.'))
        else:
            self.stdout.write(self.style.SUCCESS('User abort! Not sending emails!'))


