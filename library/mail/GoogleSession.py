import smtplib

from django.conf import settings


class GoogleSession(object):

    _smtplib = smtplib

    def __init__(self):
        self._smtpserver = GoogleSession._smtplib.SMTP("smtp.gmail.com", 587)
        self._smtpserver.ehlo()
        self._smtpserver.starttls()
        self._smtpserver.ehlo()
        self._smtpserver.login(settings.GMAIL_USER, settings.GMAIL_PASSWORD)

    @property
    def smtpserver(self):
        return self._smtpserver