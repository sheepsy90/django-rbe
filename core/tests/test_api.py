from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from core.views import create_user


class TestCoreAPI(TestCase):

    def test_identity_api_not_just_callable(self):
        c = Client()

        create_user('username', 'email', 'password')
        c.login(username='username', password='password')

        result = c.get(reverse('api_identity'))

        self.assertIn('error="invalid_token"', result._headers['www-authenticate'][1])