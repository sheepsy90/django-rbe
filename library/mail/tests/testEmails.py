import mock as mock
from django.test import TestCase

from core.views import create_user
from library.mail.NewMessageEmail import NewMessageEmail
from messaging.models import Message


class TestEmails(TestCase):

    @mock.patch('library.mail.GoogleSession.GoogleSession._smtplib')
    def test_new_message_email_new_messaging_system(self, smptlib_mock):
        smtpserver = mock.MagicMock()
        smptlib_mock.SMTP = mock.MagicMock(return_value=smtpserver)

        recipient = create_user('user', 'email', 'password')
        sender = create_user('sender', 'email', 'password')

        m = Message.create_message(sender, recipient, 'text', silent=True)

        nme = NewMessageEmail()
        nme.send(recipient_list=['emailaddress@localhost.localhost'], message=m)

        self.assertIn('https://rbe.heleska.de/messaging/conversation/{}'.format(m.sender.id), smtpserver.sendmail.call_args[0][2])


