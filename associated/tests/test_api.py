from __future__ import unicode_literals
import base64
import hashlib

import datetime
from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase
import oidc_provider.models as oidc_models

from associated.models import AssociatedService, SimpleClientCommunicationRequest


class TestSendoutApi(TestCase):
    def setUp(self):
        self.client_id = '1337'
        self.client_secret = '31415'
        self.oidc_client = oidc_models.Client(name='Unittest Client', client_id=self.client_id,
                                              client_secret=self.client_secret)
        self.oidc_client.save()

    def test_request_for_client_not_existing(self):
        test_client = Client()

        response = test_client.post(reverse('api_simple_sendout'), {
            'client_id': 'non_existing',
            'message_text': 'My message to all'
        })

        self.assertEquals(412, response.status_code)
        self.assertEquals('{"error": "client_id not known"}', response.content)

    def test_request_with_message_text_missing(self):
        test_client = Client()

        response = test_client.post(reverse('api_simple_sendout'), {
            'client_id': '1337'
        })

        self.assertEquals(412, response.status_code)
        self.assertEquals('{"error": "message_text not valid"}', response.content)

    def test_request_with_too_short_message(self):
        test_client = Client()

        response = test_client.post(reverse('api_simple_sendout'), {
            'client_id': '1337',
            'message_text': 'To short message'
        })

        self.assertEquals(412, response.status_code)
        self.assertEquals('{"error": "message_text to short"}', response.content)

    def test_checksum_missing(self):
        test_client = Client()

        response = test_client.post(reverse('api_simple_sendout'), {
            'client_id': '1337',
            'message_text': 'Long message' * 50
        })

        self.assertEquals(412, response.status_code)
        self.assertEquals('{"error": "check_sum not given"}', response.content)

    def test_check_sum_not_matching(self):
        test_client = Client()
        message = 'Long message' * 50

        response = test_client.post(reverse('api_simple_sendout'), {
            'client_id': '1337',
            'message_text': message,
            'check_sum': 'bananenelefant'
        })

        self.assertEquals(403, response.status_code)
        self.assertEquals('{"error": "check_sum not valid"}', response.content)

    def test_assoc_service_not_setup(self):
        test_client = Client()
        message = 'Long message' * 50
        dk = hashlib.pbkdf2_hmac('sha256', message, self.client_secret, 100000)
        check_sum_verification = base64.b64encode(dk).decode()  # py3k-mode

        response = test_client.post(reverse('api_simple_sendout'), {
            'client_id': '1337',
            'message_text': message,
            'check_sum': check_sum_verification
        })

        self.assertEquals(501, response.status_code)
        self.assertEquals(response.content,
                          '{"error": "Server has encountered internal precondition problems. Please contact the team that gave you the access to this service."}')

    def test_send_out_is_stopped_by_pending(self):
        assoc_service = AssociatedService(client=self.oidc_client, enabled=True)
        assoc_service.save()

        sccr = SimpleClientCommunicationRequest(client=self.oidc_client, message_text='Some message')
        sccr.save()

        test_client = Client()
        message = 'Long message' * 50
        dk = hashlib.pbkdf2_hmac('sha256', message, self.client_secret, 100000)
        check_sum_verification = base64.b64encode(dk).decode()  # py3k-mode

        response = test_client.post(reverse('api_simple_sendout'), {
            'client_id': '1337',
            'message_text': message,
            'check_sum': check_sum_verification
        })

        self.assertEquals(409, response.status_code)
        self.assertIn('job_created', response.json())
        self.assertEquals(1, response.json()['job_id'])
        self.assertEquals('pending_job', response.json()['error'])

    def test_send_out_is_stopped_by_timeout(self):
        assoc_service = AssociatedService(client=self.oidc_client, enabled=True)
        assoc_service.save()

        sccr = SimpleClientCommunicationRequest(client=self.oidc_client, message_text='Some message',
                                                created=datetime.datetime.today(), pending=False)
        sccr.save()

        test_client = Client()
        message = 'Long message' * 50
        dk = hashlib.pbkdf2_hmac('sha256', message, self.client_secret, 100000)
        check_sum_verification = base64.b64encode(dk).decode()  # py3k-mode

        response = test_client.post(reverse('api_simple_sendout'), {
            'client_id': '1337',
            'message_text': message,
            'check_sum': check_sum_verification
        })

        self.assertEquals(409, response.status_code)
        self.assertEquals('timeout_period', response.json()['error'])
        timeout_seconds = response.json()['job_timeout']
        self.assertTrue(timeout_seconds > 100)

    def test_save_send_out_request(self):
        assoc_service = AssociatedService(client=self.oidc_client, enabled=True)
        assoc_service.save()

        test_client = Client()
        message = 'Long message' * 50
        dk = hashlib.pbkdf2_hmac('sha256', message, self.client_secret, 100000)
        check_sum_verification = base64.b64encode(dk).decode()  # py3k-mode

        response = test_client.post(reverse('api_simple_sendout'), {
            'client_id': '1337',
            'message_text': message,
            'check_sum': check_sum_verification
        })

        self.assertEquals(202, response.status_code)
        self.assertEquals(response.json()['job_id'], 1)
        self.assertEquals(response.json()['job_description'],
                          'The message was accepted and wil be checked. Once released it will be send to the desired group of users')
        self.assertIn('job_created', response.json())

        job_id = response.json()['job_id']

        sccr = SimpleClientCommunicationRequest.objects.get(id=job_id)
        self.assertEquals(sccr.client, self.oidc_client)
        self.assertTrue(sccr.pending)
