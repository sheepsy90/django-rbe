from django.shortcuts import render_to_response

from library.mail.GoogleEmailCommand import GoogleEmail


class InvitationEmail(GoogleEmail):

    required_fields = ['recipient_list', 'username', 'key']

    @property
    def subject(self):
        return '[RBE Network] Invite'

    def body(self, variables):
        return render_to_response('emails/invitation_mail.html', variables).content
