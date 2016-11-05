import datetime

from django.conf.global_settings import LANGUAGES
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, default=None, related_name='user')
    invited_by = models.ForeignKey(User, related_name='invited_by', null=True)
    about_me_text = models.TextField(max_length=3000, default='')
    avatar_link = models.URLField(blank=True)


class LanguageSpoken(models.Model):
    user = models.ForeignKey(User)
    language = models.CharField(max_length=10, choices=LANGUAGES)

    @property
    def language_display(self):
        return dict(LANGUAGES)[self.language]