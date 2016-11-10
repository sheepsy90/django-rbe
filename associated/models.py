from django.db import models


class AssociatedService(models.Model):
    display_name = models.CharField(max_length=64, help_text="Display name")
    enabled = models.BooleanField(default=False, help_text="Whether the associated service is enabled or not.")