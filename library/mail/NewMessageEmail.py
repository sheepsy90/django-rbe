from django.shortcuts import render_to_response

from core.models import Toggles
from library.mail.GoogleEmailCommand import GoogleEmail


class NewMessageEmail(GoogleEmail):

    required_fields = ['recipient_list', 'message']

    @property
    def subject(self):
        return "[RBE Network] New message"

    def body(self, variables):
        message = variables['message']
        user = variables['message'].recipient

        if Toggles.is_active('new_messaging', user):
            return render_to_response('emails/new_message_email2.html', variables).content
        else:
            variables.update({
                'username': user.username,
                'message_id': message.id
            })
            return render_to_response('emails/new_message_email.html', variables).content


