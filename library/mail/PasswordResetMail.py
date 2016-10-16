from library.mail.GoogleEmailCommand import GoogleEmail


class PasswordResetMail(GoogleEmail):

    required_fields = ['recipient_list', 'username', 'reset_key', 'valid_until']

    @property
    def subject(self):
        return '[RBE Network] Password reset'

    @property
    def body(self):
        return '''Hey {username},<br>

            <p>this is an password reset to the RBE Network.</p>

            <p>If you did not expect this email please just discard it, it was probably a typo.</p>

            <p>Otherwise you can get to the password reset page following the link to:<br>
            <a href="https://rbe.heleska.de/core/chpw/{reset_key}">https://rbe.heleska.de/core/chpw/{reset_key}</a></p>

            <p>The link will be valid until: {valid_until}</p>

            <p>Kind regards,<br>
            RBE Network<br>
            https://rbe.heleska.de</p>
        '''