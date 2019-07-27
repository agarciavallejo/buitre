import pytest

from ....app.utils.email import EmailFactory
from ....app.routes import app


def test_create_user_recovery_email_returns_email():
    with app.app_context():
        email = EmailFactory.create_user_recovery_email("Andreu", "andreu@buitre.com", "token")
        assert type(email).__name__ == "Email"


def test_create_user_recovery_email_subject():
    with app.app_context():
        email = EmailFactory.create_user_recovery_email("Andreu", "andreu@buitre.com", "token")
        assert email.subject == 'BUITRE | Recover your account'


def test_create_user_recovery_email_recipient():
    with app.app_context():
        email = EmailFactory.create_user_recovery_email("Andreu", "andreu@buitre.com", "token")
        assert email.recipients == ["andreu@buitre.com"]