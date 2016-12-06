from django.shortcuts import render_to_response

from library.mail.GoogleEmailCommand import GoogleEmail


class NewMessageEmail(GoogleEmail):

    def __init__(self, google_session=None):
        GoogleEmail.__init__(self, google_session)

    required_fields = ['recipient_list', 'message']

    @property
    def subject(self):
        return "[RBE Network] New message"

    def body(self, variables):
        return render_to_response('emails/new_message_email2.html', variables).content



