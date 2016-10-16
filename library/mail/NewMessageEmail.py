from library.mail.GoogleEmailCommand import GoogleEmail


class NewMessageEmail(GoogleEmail):

    required_fields = ['recipient_list', 'username', 'message_id']

    @property
    def subject(self):
        return "[RBE Network] New message"

    @property
    def body(self):
        return '''Hey {username},<br>

                <p>you got a message from someone on the RBE Network. To check it out please visit:<br>
                <a href="https://rbe.heleska.de/messaging/message/{message_id}">https://rbe.heleska.de/messaging/message/{message_id}</a></p>

                <p>The feature to disable those emails will be soon implemented.<br>
                ----</p>

                <p>If you did not expect this email please just discard it, it was probably a typo.</p>

                <p>Kind regards,<br>
                RBE Network<br>
                https://rbe.heleska.de</p>
        '''