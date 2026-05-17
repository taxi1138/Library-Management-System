from classes.Customer import Customer
from classes.Person import Person
from classes.Book import Book
import pandas as pd
import os


class Librarian(Person):
	login_pass_Librarian = {}
	Librarians = []
	librarian_ID = 0

	def __init__(self,name,age,password,nickname):
		super().__init__(name,age)
		self.id = self.librarian_ID
		if self.age < 18:
			raise ValueError("You cannot become a Librarian before you turn 18!")
		self.verify_password(password)
		self.verify_nickname(nickname)
		self.login_pass_Librarian[f"{self.nickname}"] = self.password
		self.Librarians.append(self)
		self.librarian_ID += 1


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


	def verify_nickname(self,nickname):
		while (not isinstance(nickname, str)) or (nickname in self.login_pass_Librarian.keys()):
			print("nickname can include special symbols and digits, but it must be of type String!")
			print("Maybe your nickname has already been taken by someone.")
			print("Try again.", end = " ")
			nickname = input("New nickname: ")
		self.nickname = nickname

	def verify_password(self,password):
		while (not isinstance(password, str)) or len(password)<6:
			print("Password must be of String type and at length 6 symbols in length!")
			print("Try again.", end = " ")
			password = input("New password: ")
		self.password = password

