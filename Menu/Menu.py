from Menu.Menu_functions import Menu_functions
from classes.Customer import Customer
from classes.Librarian import Librarian
from classes.Book import Book
import pandas as pd
import os
import ast
from decorators.decorator import decorator
import csv

class Menu(Menu_functions):
	isLibrarian = False
	isCustomer = False
	user = None


	def load_data(self):
		Books_rows = pd.read_csv("filtered_books.csv", quoting=csv.QUOTE_MINIMAL).to_dict(orient = "records")
		customers_rows = pd.read_csv("Customers_data.csv").to_dict(orient = "records")
		Librarians_rows = pd.read_csv("Librarians_data.csv").to_dict(orient = "records")

		for row in Books_rows:
			Book(row["title"],ast.literal_eval(row["authors"]),row["publication_date"],ast.literal_eval(row["genres"]))

		for row in customers_rows:
			Customer(row["ID"],row["Name"],row["Age"],ast.literal_eval(row["Borrowed books"]),row["Password"],row["Nickname"])

		for row in Librarians_rows:
			Librarian(row["ID"],row["Name"],row["Age"],row["Password"],row["Nickname"])


	def login(self):
		decision = input("are you a Customer or Librarian? (answers - c or l): ")
		if decision == "c":
			self.isCustomer = True
		elif decision == "l":
			self.isLibrarian = True
		else:
			raise ValueError("Invalid answer. You only have 2 choices: c=customer, l=librarian")

		decision = input("Do you have an account? (yes/no): ")
		if decision.lower() == "yes":
			login = input("Input login: ")
			password = input("Input password")
			if self.isLibrarian:
				if login in Librarian.login_pass_Librarian.keys():
					if Librarian.login_pass_Librarian[login] == password:
						return "Welcome back, Librarian!"
					else:
						raise ValueError("Invalid nickname or password!")
				else:
					raise ValueError("There is no Librarian with such nickname in the database")
			else:
				if login in Customer.login_pass_Customer.keys():
					if Customer.login_pass_Customer[login] == password:
						return "Welcome back, Customer!"
					else:
						raise ValueError("Invalid password!")
				else:
					raise ValueError("There is no Customer with such nickname in the database")
		elif decision.lower() == "no":
			print("///////////////////////////")
			print("REGISTRATION:")
			name = input("Input name: ")
			age = input("Input age: ")
			nickname = input("Input nickname: ")
			password = input("Input password: ")
			if self.isLibrarian:
				user = Librarian("",name,age,password,nickname)
				self.save_Librarian(user)
			else:
				user = Customer("",name,age,[],password,nickname)
				self.save_Customer(user)
			print("REGISTRATION COMPLETED")
			print(f"Welcome, {name}!")


	@decorator
	def assign_book(self,book,user):
		if book.borrowed == 0:
			if self.isCustomer:
				book.borrowed = 1
				user.books_borrowed.append(book)
				print(f"The book {book.title} is now yours, but dont forget to return it.")
			else:
				print(f"You don't have to ask, Librarian. The book {book.title} is yours.")
		else:
			print(f"Sorry, you cannot borrow this book, someone has already taken it.")



	def return_book(self,book,user):
		if book in user.books_borrowed:
			book.borrowed = 0
			user.books_borrowed.remove(book)
			print(f"You returned the book {book.title}.")
		else:
			print(f"You cannot return the book {book.title} since you never borrowed it.")


	def searchByGenre(self):
		decision = input("Are you looking for books with single genre or multiple genres? (single/mult): ")
		if decision.lower() == "single":
			genre = input("Input the genre you are looking for(First letters must be capital): ")
			print(f"These are the books with the genre {genre}:")
			for book in Book.storage:
				if genre in book.genres:
					print(book)
			book_id = input("Input the id of the book you liked: ")
			for book in Book.storage:
				if book.id == book_id:
					if not self.isLibrarian:
						self.isLibrarian = True
						self.assign_book(book)
						self.isLibrarian = False
					else:
						self.assign_book(book)


	@decorator
	def add_book(self):
		title = input("Input the title of the book: ")
		authors_num = int(input("Input the amount of authors the book has: "))
		authors = []
		for i in range(authors_num):
			author = input(f"Input author {i}:")
			authors.append(author)
		date = input("Input publication date in the format MM/DD/YY: ")
		genres_num = int(input("How many genres does the book have?: "))
		genres = []
		for i in range(genres_num):
			genre = input(f"Input genre {i}: ")
			genres.append(genre)
		book = Book(title, authors, date, genres)
		self.save_book(book)
		print(f"The book {title} was added to the database.")



	def save_Librarian(self,user):
		data = {"ID": [user.id], "Name": [user.name], "Age": [user.age], "Nickname":[user.nickname],"Password":[user.password]}
		df = pd.DataFrame(data)
		df.to_csv("Librarians_data.csv", mode="a", header=not os.path.exists("Librarians_data.csv"), index=False)


	def save_Customer(self,user):
		data = {"ID": [user.id], "Name": [user.name], "Age": [user.age], "Borrowed books": [user.books_borrowed], "Nickname":[user.nickname], "Password":[user.password]}
		df = pd.DataFrame(data)
		df.to_csv("Customers_data.csv", mode="a", header=not os.path.exists("Customers_data.csv"), index=False)


	def save_book(self,book):
		data = {"title": [book.title], "publication_date": [book.publication_date], "authors": [book.authors],
				"genres": [book.genres], "borrowed": [book.borrowed]}
		df = pd.DataFrame(data)
		df.to_csv("filtered_books.csv", mode="a", header=not os.path.exists("filtered_books.csv"))



