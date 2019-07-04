from flask import url_for
from flask_mail import Mail, Message
from ..routes import app


class Email:

    def __init__(self, subject, body, recipients, sender):
        self.subject = subject
        self.body = body
        self.recipients = recipients
        self.sender = sender


class EmailFactory:

    @staticmethod
    def create_user_validation_email(user_name, user_email, validation_token):
        subject = 'BUITRE | Validate your user account' 
        body = 'Hello ' + user_name + ',<br>welcome to BUITRES. Please follow the link below to ' \
            'complete your registration:<br><a href="' + url_for('user_api.validate_user', id=validation_token) + '"> here</a>'

        email = Email(subject, body, [user_email], 'noreply@buitre.com')
        return email


class EmailSender:

    @staticmethod
    def send(email):
        mail = Mail(app)

        message = Message(
            email.subject,
            sender=email.sender,
            recipients=email.recipients
        )
        message.html = email.body
        print(message)
        mail.send(message)
