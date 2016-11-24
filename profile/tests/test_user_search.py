from django.core.urlresolvers import reverse
from django.test import Client
from django.test import TestCase

from core.views import create_user
from profile.models import UserProfile


class TestUserSearch(TestCase):

    def test_user_search(self):
        create_user('user1', 'email', 'password')
        create_user('user2', 'email', 'password')
        create_user('user4', 'email', 'password')

        user = create_user('user3', 'email', 'password')
        userprofile = UserProfile.objects.get(user=user)

        c = Client()
        c.login(username='user1', password='password')

        response = c.get(reverse('profile-overview'), {
            'search_query': 'user3'
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['search_query'], 'user3')

        user_qs = response.context['profiles']

        self.assertEqual(len(user_qs.object_list), 1)
        self.assertEqual(user_qs.object_list, [userprofile])

