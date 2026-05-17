from abc import ABC, abstractmethod
class Menu_functions(ABC):

	@abstractmethod
	def login(self):
		pass

	@abstractmethod
	def assign_book(self, book, customer):
		pass

	@abstractmethod
	def searchByGenre(self, genre):
		pass

	@abstractmethod
	def searchByGenre_and_publicationYear(self, genre, year):
		pass

	@abstractmethod
	def removeCustomer(self, customer):
		pass

	@abstractmethod
	def borrow_book(self, book):
		pass

	@abstractmethod
	def add_book(self):
		pass


