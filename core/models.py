from django.contrib.auth.models import User
from django.db import models

class PasswordResetKey(models.Model):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64, unique=True, help_text="The unique key for resetting password!")
    valid_until = models.DateTimeField(help_text="The time until this key is valid!")
