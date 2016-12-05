import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings

from library.mail.GoogleSession import GoogleSession


class GoogleEmail(object):

    _smtplib = smtplib

    required_fields = ['recipient_list']

    def __init__(self, google_session=None):
        if not google_session:
            self._google_session = GoogleSession()
        else:
            assert isinstance(google_session, GoogleSession)
            self._google_session = google_session

    def send(self, *args, **kwargs):
        for element in self.required_fields:
            assert element in kwargs

        msg = MIMEMultipart()
        msg['From'] = settings.DEFAULT_FROM_EMAIL
        msg['To'] = ','.join(kwargs['recipient_list'])
        msg['Subject'] = self.subject

        body_html = self.body(variables=kwargs)
        body = MIMEText(body_html, 'html')
        msg.attach(body)
        self._google_session.smtpserver.sendmail(settings.DEFAULT_FROM_EMAIL, kwargs['recipient_list'], msg.as_string())

    @property
    def subject(self):
        raise NotImplementedError("Please define a subject")

    def body(self, variables):
        raise NotImplementedError("Please define a body text")




