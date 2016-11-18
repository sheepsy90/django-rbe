import datetime
from django.contrib.auth.models import User
from django.db import models

from library.log import rbe_logger
from library.mail.NewMessageEmail import NewMessageEmail


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

    def inform_recipient(self):
        """ This method sends an email to the recipient in order to inform them about a new message """
        try:
            nme = NewMessageEmail()
            nme.send(recipient_list=[self.recipient.email], message=self)
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
            sent_time = datetime.datetime.now()

        m = Message(sender=sender, recipient=recipient, message_text=message_text, sent_time=sent_time)
        m.save()
        if not silent:
            m.inform_recipient()
        return m



