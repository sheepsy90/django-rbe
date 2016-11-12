import unittest

from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from core.views import create_user
from messaging.models import Message, MessageStatus


class TestNewMessaging(TestCase):

    def test_simple_message_sending_works_and_redirects_correctly(self):
        c = Client()

        recipient = create_user('recipient', 'email', 'password')

        sender = create_user('username', 'email', 'password')
        c.login(username='username', password='password')

        response = c.post(reverse('send'), {
            'recipient_id': recipient.id,
            'message_text': 'test_message'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Message.objects.all().count(), 1)

        message = Message.objects.all().first()
        self.assertEqual(message.sender, sender)
        self.assertEqual(message.recipient, recipient)
        self.assertEqual(message.message_text, 'test_message')
        self.assertEqual(message.subject, '')
        self.assertEqual(message.status, MessageStatus.UNREAD)

        self.assertEquals(response.context['conversation_partner'], recipient)
        self.assertEquals(response.context['messages'][0], message)
        self.assertEquals(response.context['error_message'], '')

        self.assertEquals(response.context['latest_conversations'][0]['unread_messages'], 0)
        self.assertEquals(response.context['latest_conversations'][0]['user'], recipient)

    def test_confirming_unread_works(self):
        recipient = create_user('recipient', 'email', 'password')
        sender = create_user('sender', 'email', 'password')

        m = Message.create_message(sender, recipient, '', 'text', silent=True)
        self.assertEqual(m.status, MessageStatus.UNREAD)

        c = Client()
        c.login(username='recipient', password='password')

        qd = MultiValueDict({'message_ids[]': [m.id]})
        response = c.post(reverse('messaging_confirm_read'), qd)

        self.assertEqual(response.status_code, 200)

        m.refresh_from_db()
        self.assertEqual(m.status, MessageStatus.READ)

    def test_retrieving_messages_page_works_without_messages(self):
        create_user('user', 'email', 'password')

        c = Client()
        c.login(username='user', password='password')

        response = c.get(reverse('messages'))

        self.assertEqual(response.status_code, 200)


