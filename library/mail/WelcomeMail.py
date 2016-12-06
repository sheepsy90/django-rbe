from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from library.mail.Mail import Mail


class WelcomeMail(Mail):

    def __init__(self, user):
        assert isinstance(user, User), "Not an auth.User model"
        self.user = user

    def subject(self):
        return '[RBE Network] Welcome'

    def to_email(self):
        return self.user.email

    def body_html(self):
        return render_to_response('emails/welcome_mail.html', {
            'username': self.user.username}).content