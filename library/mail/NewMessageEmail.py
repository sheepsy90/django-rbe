from django.shortcuts import render_to_response

from library.mail.GoogleEmailCommand import GoogleEmail


class NewMessageEmail(GoogleEmail):

    required_fields = ['recipient_list', 'username', 'message_id']

    @property
    def subject(self):
        return "[RBE Network] New message"

    def body(self, variables):
        return render_to_response('emails/new_message_email.html', variables).content


