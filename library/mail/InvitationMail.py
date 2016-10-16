from library.mail.GoogleEmailCommand import GoogleEmail


class InvitationEmail(GoogleEmail):

    required_fields = ['recipient_list', 'username', 'key']

    @property
    def subject(self):
        return '[RBE Network] Invite'

    @property
    def body(self):
        return '''Hey,<br>
            <p>this is an invite to the RBE Network from {username}.</p>

            <p>If you did not expect this email please just discard it, it was probably a typo.</p>

            <p>Otherwise you can get to the registration page by following the link to:<br>
            <a href="https://rbe.heleska.de/core/register/{key}">https://rbe.heleska.de/core/register/{key}</a></p>

            <p>Kind regards,<br>
            RBE Network<br>
            https://rbe.heleska.de</p>
        '''