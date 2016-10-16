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
    reply_to = models.ForeignKey('self', null=True, default=None, help_text="The reply_to field that indicates that the message was an reply to a previous one")
    subject = models.CharField(max_length=120, help_text='Subject of message')
    message_text = models.CharField(max_length=1200, help_text='The actual message text')
    sent_time = models.DateTimeField(auto_now=True, help_text='The datetime when the message was sent')
    open_time = models.DateTimeField(null=True, default=None, help_text='The datetime when the message was read')

    def inform_recipient(self):
        """ This method sends an email to the recipient in order to inform them about a new message """
        try:
            nme = NewMessageEmail()
            nme.send(recipient_list=[self.recipient.email], username=self.recipient.username, message_id=self.id)
        except :
            rbe_logger.error("Could not send new message email to {}".format(self.recipient.email))

    @staticmethod
    def create_message(sender, recipient, subject, message_text):
        """ Method that actually creates the message and then triggers the informing of the user
            This later makes also some assumption when we add thread based messages.
            :param sender: the user sending the message
            :param recipient: the user receiving the message
            :param subject: The subject of the message
            :param message_text: The text of the message
            :return: the model of the message that was created
        """

        m = Message(sender=sender, recipient=recipient, subject=subject, message_text=message_text)
        m.save()
        m.inform_recipient()
        return m



