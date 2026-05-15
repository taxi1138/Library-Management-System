from classes.Customer import Customer
from classes.Person import Person
from classes.Book import Book


class Librarian(Person):
	Librarians = []

	def __init__(self,name,age,password,nickname):
		super().__init__(name,age,nickname,password)
		if self.age < 18:
			raise ValueError("You cannot become a Librarian before you turn 18!")
		self.Librarians.append(self)


	def get_info(self):
		return f"A Librarian of Name:{self.name} and Age:{self.age}"


	def assign_book(self,book,customer):
		if not isinstance(book, Book):
			raise TypeError("book must be of Book class!")
		if not isinstance(customer, Customer):
			raise TypeError("customer must be of Customer class")
		if not book.borrowed:
			book.borrowed = True
			customer.books_borrowed.append(book)
			print("")
		else:
			print(f"The book {book.title} has already been taken by someone")


