from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http.response import JsonResponse
from django.test import TestCase
from django.test.client import Client

from core.tests import create_api_preconditions_with_scope
from core.views import create_user


class TestCoreAPI(TestCase):

    def test_identity_api_not_just_callable(self):
        c = Client()

        create_user('username', 'email', 'password')
        c.login(username='username', password='password')

        result = c.get(reverse('api_identity'))

        self.assertEquals(result.status_code, 401)
        self.assertIn('error="invalid_token"', result._headers['www-authenticate'][1])

    def test_identity_api_returns_correct_value(self):
        user = create_user('username', 'email', 'password')
        bearer = create_api_preconditions_with_scope(user, ['identity'])

        c = Client()
        c.login(username='username', password='password')

        result = c.get(reverse('api_identity'), HTTP_AUTHORIZATION='Bearer {}'.format(bearer))

        self.assertEquals(result.status_code, 200)
        assert isinstance(result, JsonResponse)
        self.assertDictEqual(result.json(), {
            u'email': u'email',
            u'uid': 1,
            u'first_name': u'',
            u'last_name': u'',
            u'email_verified': False,
            u'username': u'username'})
