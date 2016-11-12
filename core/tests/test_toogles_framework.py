import uuid

from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from core.models import Toggles
from core.views import create_user
from django.core.cache import cache

class TestTogglesFramework(TestCase):

    def tearDown(self):
        """ We need to clear the cache between tests as this can interfere with the results"""
        cache.clear()

    def test_toggle_active_happy_path(self):
        user1 = create_user('username1', 'email1', 'password1')
        user2 = create_user('username2', 'email2', 'password2')

        gdevs = Group(name='developer')
        gdevs.save()

        t = Toggles(toggle_name='sample_toggle_one')
        t.save()

        user2.groups.add(gdevs)

        self.assertFalse(Toggles.is_active('sample_toggle_one', user2))
        self.assertFalse(Toggles.is_active('sample_toggle_one', user1))

        Toggles.activate(t, gdevs)

        self.assertTrue(Toggles.is_active('sample_toggle_one', user2))
        self.assertFalse(Toggles.is_active('sample_toggle_one', user1))

    def test_context_processor_toggle_not_active(self):
        c = Client()

        t = Toggles(toggle_name='sample_toggle_one')
        t.save()

        create_user('username', 'email', 'password')
        c.login(username='username', password='password')

        response = c.get(reverse('error_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated())
        self.assertDictEqual(response.context['toggles'], {u'sample_toggle_one': False})

    def test_context_processor_toggle_active_for_all(self):
        c = Client()

        t = Toggles(toggle_name='sample_toggle_one')
        t.save()

        all_users, created = Group.objects.get_or_create(name='all_users')
        t.activated_for.add(all_users)

        create_user('username', 'email', 'password')
        c.login(username='username', password='password')

        response = c.get(reverse('error_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_authenticated())
        self.assertDictEqual(response.context['toggles'], {u'sample_toggle_one': True})

