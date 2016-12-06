from django.conf import settings
from django.shortcuts import render_to_response

from library.log import rbe_logger
from library.mail.GoogleEmailCommand import GoogleEmail

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class AdminMail(GoogleEmail):

    def __init__(self, google_session):
        GoogleEmail.__init__(self, google_session)

    def send(self, subject, body, recipient_list):
        content = render_to_response('emails/admin_mail.html', {'username': 'XXXUSERNAMEYYY', 'body': body}).content

        for username, email in recipient_list:
            msg = MIMEMultipart()
            msg['From'] = settings.DEFAULT_FROM_EMAIL
            msg['Subject'] = subject
            msg['To'] = email

            specific_content = content.replace('XXXUSERNAMEYYY', username)
            mime_text = MIMEText(specific_content, 'html')
            msg.attach(mime_text)

            self._google_session.smtpserver.sendmail(settings.DEFAULT_FROM_EMAIL, [email], msg.as_string())
            rbe_logger.info("Send out admin email to user={} at email={}".format(username, email))