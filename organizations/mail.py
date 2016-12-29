from django.conf import settings

from library.mail.Mail import Mail


class OrganizationCreateNotification(Mail):

    def __init__(self, organization):
        self.organization = organization

    def subject(self):
        return "[RBE Network] Organization created"

    def body_html(self):
        return """Hey, there was a new organization you should look at: name={} website={} contact_email={}""".format(
            self.organization.name, self.organization.website_url, self.organization.contact_email)

    def to_email(self):
        return settings.ADMIN_EMAIL