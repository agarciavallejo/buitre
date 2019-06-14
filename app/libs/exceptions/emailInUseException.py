class EmailInUseException(Exception):

	def __init__(self):
		message = 'email already in use'
		super().__init__(message)
		self.message = message