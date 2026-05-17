from Menu.Menu_functions import Menu_functions
from classes.Customer import Customer
from classes.Librarian import Librarian
from classes.Book import Book
import pandas as pd
import os
import ast

class Menu(Menu_functions):
	isLibrarian = False
	isCustomer = False


	def load_data(self):
		Books_rows = pd.read_csv("filtered_books.csv").to_dict(orient = "records")
		customers_rows = pd.read_csv("Customers_data.csv").to_dict(orient = "records")
		Librarians_rows = pd.read_csv("Librarians_data.csv").to_dict(orient = "records")

		for row in Books_rows:
			book = Book(row["title"],ast.literal_eval(row["authors"]),row["publication_date"],ast.literal_eval(row["genres"]),row["borrowed"])

		for row in customers_rows:
			customer = Customer(row["ID"],row["Name"],row["Age"],ast.literal_eval(row["Borrowed books"]),row["Password"],row["Nickname"])

		for row in Librarians_rows:
			librarian = Librarian(row["ID"],row["Name"],row["Age"],row["Password"],row["Nickname"])


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

