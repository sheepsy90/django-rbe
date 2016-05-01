from django.contrib.auth.models import User
from django.db import models

class Tag(models.Model):
    value = models.CharField(max_length=64, help_text='A short meaningful word.')

    def __str__(self):
        return self.value

# Create your models here.
class Object(models.Model):

    unique_identifier = models.AutoField(primary_key=True, auto_created=True,
                                         help_text="A unique id used to create a bar code and identify the item.")
    registration_date = models.DateField(auto_now=True, help_text="The registration date of the item.")
    title = models.CharField(max_length=60, blank=False, default='', help_text="A title that briefly describes the object.")
    description = models.TextField(max_length=1000, default='', help_text="A longer initial description if necessary "
                                                                    "to specify the object in more detail.")

    entered_by = models.ForeignKey(User, help_text='The user entering this object!', null=True, default=None)
    transport = models.BooleanField(default=True, help_text='State whether the object should be transported or stay locally.')

    tags = models.ManyToManyField(Tag, help_text='Tags to find this object easily')

    def __str__(self):
        return "{} // {} // {}".format(self.unique_identifier, self.registration_date, self.short_description)


class Event(models.Model):
    """ The parent model class for all events that can happen to the object """
    object = models.ForeignKey(Object, help_text='The object which the event happened to.')
    registration_date = models.DateField(auto_now=True, help_text="The registration date of the event.")




