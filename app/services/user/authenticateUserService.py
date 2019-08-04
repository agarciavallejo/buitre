from ...utils.exceptions import ArgumentException


class AuthenticateUserService():

    def __init__(self, token_verifier):
        self.verify_token = token_verifier

    def call(self, args):
        if 'token' not in args or args['token'] is None:
            raise ArgumentException('missing token parameter')

        token = args['token']

        return self.verify_token(token)



