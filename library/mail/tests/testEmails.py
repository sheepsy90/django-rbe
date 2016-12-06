from django.test import TestCase

from core.views import create_user
from library.mail.NewMessageEmail import NewMessageEmail
from messaging.models import Message


class TestEmails(TestCase):

    def test_new_message_email_new_messaging_system(self):
        recipient = create_user('user', 'email', 'password')
        sender = create_user('sender', 'email', 'password')

        m = Message.create_message(sender, recipient, 'text', silent=True)

        nme = NewMessageEmail(m)

        self.assertIn('https://rbe-network.org/messaging/conversation/{}'.format(m.sender.id), nme.body_html())


