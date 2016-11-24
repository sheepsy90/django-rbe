from django.db import models
from oidc_provider.models import Client


class AssociatedService(models.Model):
    client = models.OneToOneField(Client)
    enabled = models.BooleanField(default=False, help_text="If the client is enabled or not.")
    description = models.TextField(default='', help_text="A description of what the client does.")
    logo_url = models.URLField(blank=True, help_text="A URL to the logo of the associated page.")

    def __str__(self):
        return "{} // {} // {}".format(self.client.name, self.client.website_url, self.enabled)