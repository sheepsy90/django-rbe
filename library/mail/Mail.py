from django.conf import settings


class Mail(object):

    def to_email(self):
        return NotImplementedError()

    def from_email(self):
        return settings.DEFAULT_FROM_EMAIL

    def body_html(self):
        raise NotImplementedError()

    def subject(self):
        raise NotImplementedError()