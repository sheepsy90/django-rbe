import datetime
from django.contrib.auth.models import User, Group
from django.core.cache import caches
from django.db import models

from library.log import rbe_logger


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


class Toggles(models.Model):
    toggle_name = models.CharField(max_length=60, unique=True, primary_key=True)
    activated_for = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return self.toggle_name

    @staticmethod
    def all_toggle_names():
        cache = caches['default']
        result = cache.get('all_toggle_names')
        if result is None:
            result = Toggles.objects.all().values_list('toggle_name', flat=True)
            cache.set('all_toggle_names', result)
        return result

    @staticmethod
    def is_active(toggle_name, user):
        cache = caches['default']

        active_for_groups = cache.get('toggle_{}_active_for'.format(toggle_name))

        # If the result from cache is none we need to refill the cache
        if active_for_groups is None:
            try:
                toggle = Toggles.objects.get(toggle_name=toggle_name)
                active_for_groups = toggle.activated_for.all().values_list('name', flat=True)
                cache.set('toggle_{}_active_for'.format(toggle_name), active_for_groups)
            except Toggles.DoesNotExist:
                rbe_logger.warning("Tried to access a toggle name that doesn't exists: {}".format(user))
                return False

        user_group_list = user.groups.all().values_list('name', flat=True)

        # If it is still None return False
        intersection = set(user_group_list).intersection(set(active_for_groups))
        return len(intersection) > 0

    @staticmethod
    def invalidate_cache(toggle_name):
        cache = caches['default']
        cache.delete('toggle_{}_active_for'.format(toggle_name))
        cache.delete('all_toggle_names')

    @staticmethod
    def activate(toggle, group):
        toggle.activated_for.add(group)
        Toggles.invalidate_cache(toggle.toggle_name)
