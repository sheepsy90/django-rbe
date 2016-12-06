from __future__ import unicode_literals

import sendgrid
import sendgrid.helpers.mail as sg_helpers

from django.conf import settings

from library.log import rbe_logger
from library.mail.Mail import Mail


class SendgridEmailClient(object):
    def __init__(self):
        self._sendgrid_client = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

    def send_mail(self, mail_object, overwrite_to=None):
        assert isinstance(mail_object, Mail), "Was not a Mail object"

        from_email = sg_helpers.Email(mail_object.from_email())

        if overwrite_to:
            to_email = sg_helpers.Email(overwrite_to)
        else:
            to_email = sg_helpers.Email(mail_object.to_email())

        content = sg_helpers.Content("text/html", mail_object.body_html())

        mail = sg_helpers.Mail(from_email, mail_object.subject(), to_email, content)
        response = self._sendgrid_client.client.mail.send.post(request_body=mail.get())

        if response.status_code == 202:
            rbe_logger.info(
                "Send {} email successful to {}".format(mail_object.__class__.__name__, mail_object.from_email()))
        else:
            rbe_logger.error(
                "Send {} email failed with status_code={} successful to {}".format(mail_object.__class__.__name__,
                                                                                   response.status_code,
                                                                                   mail_object.from_email()))
