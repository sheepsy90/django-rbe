import datetime
import json
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from library.log import rbe_logger
from library.mail.NewMessageEmail import NewMessageEmail
from library.mail.SendgridEmailClient import SendgridEmailClient


class MessageStatus:
    UNREAD = 0
    READ = 1
    DELETED = 2


class Message(models.Model):
    sender = models.ForeignKey(User, help_text="The user who send the message", related_name='sender')
    recipient = models.ForeignKey(User, help_text="The user who shall receive the message", related_name='recipient')
    status = models.IntegerField(default=MessageStatus.UNREAD, help_text="The message status - determines how the message is displayed")
    message_text = models.CharField(max_length=1200, help_text='The actual message text')
    sent_time = models.DateTimeField(blank=True, null=True, help_text='The datetime when the message was sent')

    def __str__(self):
        return "From: {} // To: {}".format(self.sender, self.recipient)

    def inform_recipient(self):
        """ This method sends an email to the recipient in order to inform them about a new message """
        try:
            sg = SendgridEmailClient()
            nme = NewMessageEmail(self)
            sg.send_mail(nme)
        except :
            rbe_logger.error("Could not send new message email to {}".format(self.recipient.email))

    @staticmethod
    def create_message(sender, recipient, message_text, sent_time=None, silent=False):
        """ Method that actually creates the message and then triggers the informing of the user
            This later makes also some assumption when we add thread based messages.
            :param sender: the user sending the message
            :param recipient: the user receiving the message
            :param subject: The subject of the message
            :param message_text: The text of the message
            :return: the model of the message that was created
        """
        if not sent_time:
            sent_time = timezone.now()

        last_message = Message.objects.filter(sender=sender, recipient=recipient).order_by('-sent_time')

        if last_message.count() > 0:
            last_sent_time = last_message.first().sent_time
            half_hour_ago = timezone.now() - timezone.timedelta(minutes=30)
            should_inform_recipient = last_sent_time < half_hour_ago
        else:
            should_inform_recipient = True

        m = Message(sender=sender, recipient=recipient, message_text=message_text, sent_time=sent_time)
        m.save()

        if not silent and should_inform_recipient:
            m.inform_recipient()

        return m


class ChatMessage(models.Model):
    author = models.ForeignKey(User, help_text="The user who send the message")
    message = models.CharField(max_length=1200, help_text='The actual message text')
    sent_time = models.DateTimeField(blank=True, null=True, help_text='The datetime when the message was sent')

    @property
    def as_payload(self):
        return {
            "text": json.dumps({
                'type': 'message_received',
                'user': self.author.username,
                'message': self.message,
                'sent_time': self.sent_time.strftime('%Y-%m-%d %H:%M %Z'),
            })
        }
