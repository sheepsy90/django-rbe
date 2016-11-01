from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class SlugPhrase(models.Model):
    value = models.CharField(max_length=128, blank=True, unique=True)

    def __unicode__(self):
        return self.value


class UserSlugs(models.Model):
    user = models.ForeignKey(User)
    slug = models.ForeignKey(SlugPhrase)


class UserSkill(models.Model):
    user = models.ForeignKey(User)
    slug = models.ForeignKey(SlugPhrase)
    level = models.IntegerField(default=3, validators=[MaxValueValidator(5), MinValueValidator(1)])
    latest_change = models.DateTimeField(auto_now=True)

