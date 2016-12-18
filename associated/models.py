from django.contrib.auth.models import User
from django.db import models
from oidc_provider.models import Client


class AssociatedService(models.Model):
    client = models.OneToOneField(Client)
    enabled = models.BooleanField(default=False, help_text="If the client is enabled or not.")
    description = models.TextField(default='', help_text="A description of what the client does.")
    logo_url = models.URLField(blank=True, help_text="A URL to the logo of the associated page.")
    sendout_day_period = models.IntegerField(default=28,
                                             help_text="The number of days until a client can send a simple message again.")

    def __str__(self):
        return "{} // {} // {}".format(self.client.name, self.client.website_url, self.enabled)


class SimpleClientCommunicationRequest(models.Model):
    """ A simple client communication request that can be pending until approved """
    client = models.ForeignKey(Client)
    message_text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    pending = models.BooleanField(default=True)


class ClientCommunicationBlocks(models.Model):
    """ This model is created if a user wants to block messages
        from a particular client """
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)
    reason = models.CharField(max_length=256)