import unittest

import datetime
import mock
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from django.utils import timezone
from django.utils.datastructures import MultiValueDict

from core.views import create_user
from messaging.models import Message, MessageStatus


class TestNewMessaging(TestCase):

    @mock.patch('library.mail.SendgridEmailClient.SendgridEmailClient')
    def test_simple_message_sending_works_and_redirects_correctly(self, smc):
        c = Client()

        recipient = create_user('recipient', 'email', 'password')

        sender = create_user('username', 'email', 'password')
        c.login(username='username', password='password')

        response = c.post(reverse('send'), {
            'recipient_id': recipient.id,
            'message_text': 'test_message'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Message.objects.all().count(), 1)

        message = Message.objects.all().first()
        self.assertEqual(message.sender, sender)
        self.assertEqual(message.recipient, recipient)
        self.assertEqual(message.message_text, 'test_message')
        self.assertEqual(message.status, MessageStatus.UNREAD)

    @mock.patch('library.mail.SendgridEmailClient.SendgridEmailClient')
    def test_confirming_unread_works(self, smc):
        recipient = create_user('recipient', 'email', 'password')
        sender = create_user('sender', 'email', 'password')

        m = Message.create_message(sender, recipient, 'text', silent=True)
        self.assertEqual(m.status, MessageStatus.UNREAD)

        c = Client()
        c.login(username='recipient', password='password')

        qd = MultiValueDict({'message_ids[]': [m.id]})
        response = c.post(reverse('messaging_confirm_read'), qd)

        self.assertEqual(response.status_code, 200)

        m.refresh_from_db()
        self.assertEqual(m.status, MessageStatus.READ)

    @mock.patch('library.mail.SendgridEmailClient.SendgridEmailClient')
    def test_retrieving_messages_page_works_without_messages(self, smc):
        create_user('user', 'email', 'password')

        c = Client()
        c.login(username='user', password='password')

        response = c.get(reverse('messages'))

        self.assertEqual(response.status_code, 200)

    @mock.patch('library.mail.SendgridEmailClient.SendgridEmailClient')
    def test_retrieving_messages_page_works_with_read_message(self, smc):
        recipient = create_user('user', 'email', 'password')
        sender = create_user('sender', 'email', 'password')

        m = Message.create_message(sender, recipient, 'text', silent=True)
        m.status = MessageStatus.READ
        m.save()

        c = Client()
        c.login(username='user', password='password')

        response = c.get(reverse('messages'))

        self.assertEqual(response.status_code, 200)

    @mock.patch('library.mail.SendgridEmailClient.SendgridEmailClient')
    def test_view_function_for_sending_message(self, smc):
        recipient = create_user('user', 'email', 'password')
        sender = create_user('sender', 'email', 'password')

        c = Client()
        c.login(username='sender', password='password')

        response = c.post(reverse('send'), {'recipient_id': recipient.id, 'message_text': 'Test message'})

        self.assertEqual(response.status_code, 302)

        mqs = Message.objects.filter(sender=sender, recipient=recipient)
        self.assertEqual(1, mqs.count())

    def test_send_is_silenced(self):
        recipient = create_user('user', 'email', 'password')
        sender = create_user('sender', 'email', 'password')

        f = Message.inform_recipient
        inform_mock = mock.MagicMock()
        Message.inform_recipient = inform_mock
        Message.create_message(sender, recipient, 'text1')

        inform_mock.assert_called_once()
        inform_mock.reset_mock()

        Message.create_message(sender, recipient, 'text2')
        inform_mock.assert_not_called()

        Message.inform_recipient = f

    def test_send_is_not_silenced_after_half_an_hour(self):
        recipient = create_user('user', 'email', 'password')
        sender = create_user('sender', 'email', 'password')

        f = Message.inform_recipient
        inform_mock = mock.MagicMock()
        Message.inform_recipient = inform_mock
        sent_time = timezone.now() - datetime.timedelta(minutes=31)
        Message.create_message(sender, recipient, 'text1', sent_time)

        inform_mock.assert_called_once()
        inform_mock.reset_mock()

        Message.create_message(sender, recipient, 'text2')
        inform_mock.assert_called_once()

        Message.inform_recipient = f
