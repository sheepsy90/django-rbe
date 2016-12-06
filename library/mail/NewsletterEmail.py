from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from library.mail.Mail import Mail


class NewsletterMail(Mail):

    def __init__(self, user, customized_body):
        Mail.__init__(self)
        assert isinstance(user, User), "User is not a auth.User model"
        self.user = user
        self.customized_body = customized_body

    def subject(self):
        return "[RBE Network] Newsletter"

    def body_html(self):
        html = render_to_response('emails/admin_mail.html', {
            'username': self.user.username,
            'body': self.customized_body}).content

        return html

    def from_email(self):
        return "RBE-Network <newsletter@mail.rbe-network.org>"

    def to_email(self):
        return self.user.email

