from core.models import Tag
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import render_to_response



class Object(models.Model):

    unique_identifier = models.AutoField(primary_key=True, auto_created=True,
                                         help_text="A unique id used to create a bar code and identify the item.")
    registration_date = models.DateTimeField(auto_now=True, help_text="The registration date of the item.")
    title = models.CharField(max_length=60, blank=False, default='', help_text="A title that briefly describes the object.")
    description = models.TextField(max_length=1000, default='', help_text="A longer initial description if necessary "
                                                                    "to specify the object in more detail.")

    entered_by = models.ForeignKey(User, help_text='The user entering this object!', null=True, default=None)
    transport = models.BooleanField(default=True, help_text='State whether the object should be transported or stay locally.')

    tags = models.ManyToManyField(Tag, related_name='object_tags')

    def __str__(self):
        return "{} // {} // {}".format(self.unique_identifier, self.registration_date, self.description)


class DummyEvent(object):

    def render(self):
        return ''


class Event(models.Model):
    """ The parent model class for all events that can happen to the object """
    object = models.ForeignKey(Object, help_text='The object which the event happened to.')
    registration_date = models.DateTimeField(auto_now=True, help_text="The registration date of the event.")
    triggered_user = models.ForeignKey(User, null=True, help_text="The user who triggered the event.")
    related_clazz = models.CharField(max_length=64, blank=True, help_text="The name of the related clazz that holds the additional data.")

    class Meta:
        index_together = [
           ["registration_date"],
        ]

    def render(self):
        raise NotImplementedError()


class TagModificationLogEvent(Event):
    """ A simple log message """
    added = models.BooleanField(default=True, help_text="Indicating if the tag was added or removed!")
    tag_name = models.CharField(max_length=64)

    @staticmethod
    def create(object, user, tag_value, added=True):
        sle = TagModificationLogEvent(object=object, triggered_user=user, tag_name=tag_value, added=added,
                                      related_clazz='TagModificationLogEvent'.lower())
        sle.save()
        return sle

    def render(self):
        response = render_to_response("timeline/tag_modification_event.html", {'event': self})
        return response.content


class SimpleObjectCommentEvent(Event):
    comment_text = models.TextField(max_length=250)

    @staticmethod
    def create(object, user, comment_text):
        sle = SimpleObjectCommentEvent(object=object, triggered_user=user, comment_text=comment_text,
                                      related_clazz='SimpleObjectCommentEvent'.lower())
        sle.save()
        return sle

    def render(self):
        response = render_to_response("timeline/simple_object_comment_event.html", {'event': self})
        return response.content