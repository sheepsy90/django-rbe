from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    invited_by = models.ForeignKey(User, related_name='invited_by', null=True)
    is_confirmed = models.BooleanField(default=False)
    about_me_text = models.TextField(max_length=3000, default='')
    avatar_link = models.URLField(blank=True)


class PasswordResetKey(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64, unique=True, help_text="The unique key for resetting password!")
    valid_until = models.DateTimeField(help_text="The time until this key is valid!")
