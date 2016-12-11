import uuid

from django.core.urlresolvers import reverse
from django.http.response import JsonResponse
from django.test import TestCase
import django.test.client as djtest
from django.utils import timezone
from oidc_provider.models import Token, Client, UserConsent

from core.views import create_user


class TestCoreAPI(TestCase):

    def test_identity_api_not_just_callable(self):
        c = djtest.Client()

        create_user('username', 'email', 'password')
        c.login(username='username', password='password')

        result = c.get(reverse('api_identity'))

        self.assertEquals(result.status_code, 401)
        self.assertIn('error="invalid_token"', result._headers['www-authenticate'][1])


    def create_api_preconditions_with_scope(self, user, scopes):
        assert isinstance(scopes, list)
        bearer = uuid.uuid4().hex

        client = Client(name='test_client')
        client.save()

        expires_at = timezone.now() + timezone.timedelta(days=30)
        t = Token(scope=scopes, access_token=bearer, user=user, expires_at=expires_at, client=client)
        t.save()

        return bearer

    def test_identity_api_returns_correct_value(self):
        user = create_user('username', 'email', 'password')
        bearer = self.create_api_preconditions_with_scope(user, ['identity'])

        c = djtest.Client()
        c.login(username='username', password='password')

        result = c.get(reverse('api_identity'), HTTP_AUTHORIZATION='Bearer {}'.format(bearer))

        self.assertEquals(result.status_code, 200)
        assert isinstance(result, JsonResponse)
        self.assertDictEqual(result.json(), {u'email': u'email', u'uid': 1, u'username': u'username'})
