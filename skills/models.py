from django.contrib.auth.models import User
from django.db import models

class SlugPhrase(models.Model):
    value = models.CharField(max_length=128, blank=True, unique=True)

    def __str__(self):
        return self.value


class UserSlugs(models.Model):
    user = models.ForeignKey(User)
    slug = models.ForeignKey(SlugPhrase)