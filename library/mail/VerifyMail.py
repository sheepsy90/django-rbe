from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render_to_response

from core.models import EmailVerification
from library.mail.Mail import Mail


class VerifyMail(Mail):

    def __init__(self, email_verification):
        assert isinstance(email_verification, EmailVerification), "Not an EmailVerification object"
        self.email_verification = email_verification

    def subject(self):
        return '[RBE Network] Verify your Email'

    def to_email(self):
        return self.email_verification.user.email

    def body_html(self):
        return render_to_response('emails/verification_email.html', {
            'email_verification': self.email_verification,
            'site_url': settings.SITE_URL,
        }).content