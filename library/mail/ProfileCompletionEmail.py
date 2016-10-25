from django.shortcuts import render_to_response

from library.mail.GoogleEmailCommand import GoogleEmail


class ProfileCompletionEmail(GoogleEmail):

    required_fields = ['recipient_list', 'username', 'location_missing', 'about_missing']

    @property
    def subject(self):
        return '[RBE Network] Complete your profile'

    def body(self, variables):
        return render_to_response('emails/profile_completion.html', variables).content
