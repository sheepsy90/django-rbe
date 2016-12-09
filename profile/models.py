from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count

from profile.constants import LANGUAGE_LEVELS


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, default=None, related_name='user')
    about_me_text = models.TextField(max_length=3000, default='')
    avatar_link = models.URLField(blank=True)

    @property
    def email_verified(self):
        return self.user.emailverification.confirmed


class LanguageSpoken(models.Model):
    user = models.ForeignKey(User)
    language = models.CharField(max_length=10, choices=LANGUAGES)
    level = models.CharField(max_length=64, choices=LANGUAGE_LEVELS, default=LANGUAGE_LEVELS[0][0])

    @property
    def language_display(self):
        return dict(LANGUAGES)[self.language]

    @property
    def level_display(self):
        return dict(LANGUAGE_LEVELS)[self.level]

    @staticmethod
    def count_grouping():
        qs = LanguageSpoken.objects.values('language').annotate(num_users=Count('user', distinct=True))
        total = LanguageSpoken.objects.count()
        [e.update({
            'language_display': dict(LANGUAGES)[e['language']],
            'percentage_count': int(100*e['num_users'] / float(total)),
        }) for e in qs]

        qs = sorted(qs, key=lambda x: -x['percentage_count'])

        return qs

    def __repr__(self):
        return u'{} / {}'.format(self.user, self.language)