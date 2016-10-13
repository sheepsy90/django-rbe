from django.contrib.auth.models import User
from django.db import models


class InvitationKey(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64, unique=True, help_text="The unique key for invite identification!")
    email = models.EmailField(max_length=128, default='', help_text="The email to send the invite too!")

    class Meta:
        unique_together = [('user', 'email')]
        db_table = 'invitation_key'


class UserProfile(models.Model):
    pass