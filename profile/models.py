from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    class Meta:
        db_table = 'profile'

    user = models.OneToOneField(User)
    invited_by = models.ForeignKey(User, related_name='invited_by2', null=True)
    is_confirmed = models.BooleanField(default=False)
    about_me_text = models.TextField(max_length=3000, default='')
    avatar_link = models.URLField(blank=True)


class RegistrationKey(models.Model):
    profile = models.ForeignKey(Profile)
    key = models.CharField(max_length=64, unique=True, help_text="The unique key for invite identification!")
    email = models.EmailField(max_length=128, default='', help_text="The email to send the invite too!")

    class Meta:
        unique_together = [('profile', 'email')]
        db_table = 'registration_key'
