from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from library.mail.Mail import Mail


class PasswordResetMail(Mail):

    def __init__(self, user, reset_key, valid_until):
        assert isinstance(user, User), "Not an auth.User model"

        self.user = user
        self.reset_key = reset_key
        self.valid_until = valid_until

    def subject(self):
        return '[RBE Network] Password reset'

    def body_html(self):
        return render_to_response('emails/password_reset_mail.html', {
            'username': self.user.username,
            'reset_key': self.reset_key,
            'valid_until': self.valid_until
        }).content

    def to_email(self):
        return self.user.email