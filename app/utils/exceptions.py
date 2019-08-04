class ArgumentException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class EmailInUseException(Exception):
    def __init__(self):
        message = 'email already in use'
        super().__init__(message)
        self.message = message


class NoValidUserException(Exception):
    def __init__(self):
        message = 'user has not been validated'
        super().__init__(message)
        self.message = message


class AuthenticationException(Exception):
    def __init__(self):
        message = 'authentication error'
        super().__init__(message)
        self.message = message


class UserValidationException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class ExpiredTokenException(Exception):
    def __init__(self):
        message = 'token is expired'
        super().__init__(message)
        self.message = message


class InvalidTokenException(Exception):
    def __init__(self):
        message = 'invalid token'
        super().__init__(message)
        self.message = message


class UserNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
