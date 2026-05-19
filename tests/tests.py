import unittest

from classes.Book import Book
from classes.Customer import Customer
from classes.Librarian import Librarian


class TestCreation(unittest.TestCase):

	def test_customer_creation(self):
		customer = Customer("", "John", 20, "", "mypassword", "john123")
		self.assertEqual(customer.name, "John")
		self.assertEqual(customer.age, 20)
		self.assertEqual(customer.books_borrowed, "")
		self.assertEqual(customer.password, "mypassword")
		self.assertEqual(customer.nickname, "john123")

	def test_librarian_creation(self):
		librarian = Librarian("", "Alice", 30, "adminpass", "aliceadmin")
		self.assertEqual(librarian.name, "Alice")
		self.assertEqual(librarian.age, 30)
		self.assertEqual(librarian.password, "adminpass")
		self.assertEqual(librarian.nickname, "aliceadmin")

	def test_book_creation(self):
		book = Book("Harry Potter",["J.K. Rowling"],"06/26/97",["Fantasy", "Adventure"],0)
		self.assertEqual(book.title, "Harry Potter")
		self.assertEqual(book.authors, ["J.K. Rowling"])
		self.assertEqual(book.publication_date, "06/26/97")
		self.assertEqual(book.genres, ["Fantasy", "Adventure"])
		self.assertEqual(book.borrowed, 0)

if __name__ == "__main__":
	unittest.main()