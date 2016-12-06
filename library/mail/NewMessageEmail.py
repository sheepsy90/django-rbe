from __future__ import unicode_literals

from django.shortcuts import render_to_response

from library.mail.Mail import Mail


class NewMessageEmail(Mail):

    def __init__(self, message):
        assert message.__class__.__name__ == 'Message', "Message is not a models.Message model"
        self.message = message

    def subject(self):
        return "[RBE Network] New message"

    def body_html(self):
        return render_to_response('emails/new_message_email2.html', {
            'message': self.message
        }).content

    def to_email(self):
        return self.message.recipient.email


