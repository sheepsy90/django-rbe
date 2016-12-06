from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from library.mail.Mail import Mail


class ProfileCompletionEmail(Mail):

    def __init__(self, user, location_missing, about_missing, language_missing):
        assert isinstance(user, User), "Not an auth.User model"

        self.user = user
        self.location_missing = location_missing
        self.about_missing = about_missing
        self.language_missing = language_missing

    def body_html(self):
        return render_to_response('emails/profile_completion.html', {
            'username': self.user.username,
            'about_missing': self.about_missing,
            'location_missing': self.location_missing,
            'language_missing': self.language_missing
        }).content

    def to_email(self):
        return self.user.email

    def subject(self):
        return '[RBE Network] Complete your profile'

