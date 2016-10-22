from django.shortcuts import render_to_response

from library.mail.GoogleEmailCommand import GoogleEmail


class TestEmail(GoogleEmail):

    @property
    def subject(self):
        return "This is a test email"

    def body(self, variables):
        variables.update({'valid_until': 'someone', 'key': 3, 'username': 'hannes'})
        return render_to_response('emails/invitation_mail.html', variables).content


