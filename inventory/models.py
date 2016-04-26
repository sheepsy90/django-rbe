from django.db import models


# Create your models here.
class Object(models.Model):

    unique_identifier = models.AutoField(primary_key=True, auto_created=True)
    registration_date = models.DateField()
    short_description = models.TextField(max_length=200)

    def __str__(self):
        return "{} // {} // {}".format(self.unique_identifier, self.registration_date, self.short_description)

class ObjectLogEntry(models.Model):
    """ A log entry saying something about the object """
    referenced_object = models.ForeignKey(Object)

    file_date = models.DateTimeField()

    content = models.TextField(max_length=3000)
