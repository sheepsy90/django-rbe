import datetime
from django.contrib.auth.models import User
from django.db import models


class PasswordResetKey(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64, unique=True, help_text="The unique key for resetting password!")
    valid_until = models.DateTimeField(help_text="The time until this key is valid!")


class LastSeen(models.Model):
    user = models.OneToOneField(User)
    date_time = models.DateTimeField(null=True, default=None)

    @property
    def last_online_class(self):

        if not self.date_time:
            return 'red'

        tdm14 = datetime.datetime.today() - datetime.timedelta(days=14)
        tdm3 = datetime.datetime.today() - datetime.timedelta(days=3)

        if self.date_time.date() < tdm14.date():
            return 'red'
        elif tdm14.date() <= self.date_time.date() < tdm3.date():
            return 'yellow'
        else:
            return 'green'