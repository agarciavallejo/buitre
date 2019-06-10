from abc import ABC, abstractmethod

class BaseService(ABC):

	@abstractmethod
	def inContract(self, args):
		pass

	@abstractmethod
	def outContract(self, args):
		pass

	@abstractmethod
	def execute(self, args):
		pass