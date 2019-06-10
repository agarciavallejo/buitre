from ..baseService import BaseService

class CreateUserService(BaseService):

	def inContract(self, args):
		if ('email' not in args):
			return "ERROR"

	def outContract(self, args):
		pass

	def execute(self, args):
		pass