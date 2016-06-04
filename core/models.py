from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    value = models.CharField(max_length=64, blank=True, unique=True)

    def __str__(self):
        return self.value


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    invited_by = models.ForeignKey(User, related_name='invited_by', null=True)
    tags = models.ManyToManyField(Tag, related_name='profile_tags')
    is_confirmed = models.BooleanField(default=False)
    about_me_text = models.TextField(max_length=3000, default='')
    avatar_link = models.URLField(blank=True)


class RegistrationKey(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64, unique=True, help_text="The unique key for invite identification!")
    email = models.EmailField(max_length=128, default='', help_text="The email to send the invite too!")

    class Meta:
        unique_together = [('user', 'email')]
