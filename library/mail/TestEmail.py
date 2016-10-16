from library.mail.GoogleEmailCommand import GoogleEmail


class TestEmail(GoogleEmail):

    @property
    def subject(self):
        return "This is a test email"

    @property
    def body(self):
        return """
        <html>
          <head></head>
          <body>
            <p>Hi!<br>
               This is a test email to check whether it works or not!<br>
            </p>
          </body>
        </html>
        """