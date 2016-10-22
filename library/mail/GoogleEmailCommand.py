import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings


class GoogleEmail(object):

    required_fields = ['recipient_list']

    def __init__(self):
        self.smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtpserver.ehlo()
        self.smtpserver.starttls()
        self.smtpserver.ehlo()
        self.smtpserver.login(settings.GMAIL_USER, settings.GMAIL_PASSWORD)

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
        self.smtpserver.sendmail(settings.DEFAULT_FROM_EMAIL, kwargs['recipient_list'], msg.as_string())

    @property
    def subject(self):
        raise NotImplementedError("Please define a subject")

    def body(self, variables):
        raise NotImplementedError("Please define a body text")




