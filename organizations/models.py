from __future__ import  unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

ROLE_CHOICES = [
    ('Editor', 'Editor'),
    ('Follower', 'Follower')
]

"""
The different roles have different rights and responsibilities.

Editor: Someone from the organization
        - Changes organization description
        - Allows people to become editors and allows members
        - Can post on the activity feed

Follower: Someone who is interested in an organization
"""


class OrganizationTag(models.Model):
    """ Specific tags (short words or phrases) describing an organization """
    value = models.SlugField()

    def __unicode__(self):
        return self.value


class Organization(models.Model):
    """ The model representing an organization """
    name = models.CharField(max_length=256, unique=True)
    logo_url = models.URLField(blank=True, null=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.CharField(max_length=255, default='', blank=True, null=True)
    enabled = models.BooleanField(default=False, help_text="Whether they are visible on the page.")
    tags = models.ManyToManyField(OrganizationTag)

    @property
    def display_tags(self):
        return ", ".join(self.tags.values_list('value', flat=True))

    def __unicode__(self):
        return "{}, enable={}".format(self.name, self.enabled)

    @property
    def can_post(self):
        """ An organization can post every two days """
        post_delay = timezone.now() - timezone.timedelta(hours=settings.POSTING_TIMEOUT_HOURS)
        return not OrganizationPost.objects.filter(organization=self, created__gte=post_delay).exists()


class OrganizationPost(models.Model):
    """ Model of a post by the organization """
    organization = models.ForeignKey(Organization)
    content = models.TextField(max_length=2000)
    created = models.DateTimeField()
    author = models.ForeignKey(User)


class OrganizationDescription(models.Model):
    """ The description of the organization which can be edited by the role: editor """
    organization = models.OneToOneField(Organization)
    summary = models.TextField(max_length=500, default='', blank=True)
    value_system = models.TextField(max_length=500, default='', blank=True)
    decision_making = models.TextField(max_length=500, default='', blank=True)
    when_join = models.TextField(max_length=500, default='', blank=True)

    def __unicode__(self):
        return "{}".format(self.organization.name)

    @property
    def none_available(self):
        return not any([self.summary, self.value_system, self.decision_making, self.when_join])


class OrganizationCheck(models.Model):
    organization = models.OneToOneField(Organization)
    last_checked = models.DateTimeField(null=True, blank=True)
    useful_content = models.CharField(max_length=32, default='?')
    uses_money = models.CharField(max_length=32, default='?')
    automation = models.CharField(max_length=32, default='?')
    project_plan = models.CharField(max_length=32, default='?')
    implementation_oriented = models.CharField(max_length=32, default='?')
    geographic_location = models.CharField(max_length=32, default='?')
    rbe_network = models.CharField(max_length=32, default='?')
    open_source = models.CharField(max_length=32, default='?')

    # The five economic model factors
    system = models.CharField(max_length=32, default='?')
    access = models.CharField(max_length=32, default='?')
    resource = models.CharField(max_length=32, default='?')
    participatory = models.CharField(max_length=32, default='?')
    monetary = models.CharField(max_length=32, default='?')

    # A note from the assesment side
    note = models.CharField(max_length=500, default='', blank=True)

    def __unicode__(self):
        return "{}".format(self.organization.name)


class OrganizationUser(models.Model):
    organization = models.ForeignKey(Organization)
    user = models.ForeignKey(User)
    level = models.CharField(max_length=32, choices=ROLE_CHOICES)

    def __unicode__(self):
        return "user={} organization=<{}> role={}".format(self.user, self.organization.name, self.level)
