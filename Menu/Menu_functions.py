from abc import ABC, abstractmethod
class Menu_functions(ABC):

	@abstractmethod
	def login(self):
		pass

	@abstractmethod
	def assign_book(self, book, customer):
		pass

	@abstractmethod
	def search_by_genre(self):
		pass

	@abstractmethod
	def advanced_search(self):
		pass

	@abstractmethod
	def search_by_author(self):
		pass

	@abstractmethod
	def add_book(self):
		pass


