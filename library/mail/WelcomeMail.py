from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from core.models import EmailVerification
from library.mail.Mail import Mail


class WelcomeMail(Mail):

    def __init__(self, user, email_verification):
        assert isinstance(user, User), "Not an auth.User model"
        assert isinstance(email_verification, EmailVerification), "Not an EmailVerification object"
        self.email_verification = email_verification
        self.user = user

    def subject(self):
        return '[RBE Network] Welcome'

    def to_email(self):
        return self.user.email

    def body_html(self):
        return render_to_response('emails/welcome_mail.html', {
            'user': self.user,
            'email_verification': self.email_verification,
            'site_url': settings.SITE_URL,
        }).content