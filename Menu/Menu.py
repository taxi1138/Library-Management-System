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
		Librarian.login_pass_Librarian = pd.read_csv("Librarians_nickname_pass.csv").set_index("Nickname")["Password"].to_dict()
		Customer.login_pass_Customer = pd.read_csv("Customers_nickname_pass.csv").set_index("Nickname")["Password"].to_dict()
		Books_rows = pd.read_csv("filtered_books.csv").to_dict(orient = "records")
		customers_rows = pd.read_csv("Customers_data.csv", usecols = ["ID","Name","Age","Borrowed books"]).to_dict(orient = "records")
		Librarians_rows = pd.read_csv("Librarians_data.csv",usecols = ["ID","Name","Age"]).to_dict(orient = "records")

		for row in Books_rows:
			book = Book(row["title"],ast.literal_eval(row["authors"]),row["publication_date"],ast.literal_eval(row["genres"]),row["borrowed"])

		for row in customers_rows:
			customer = Customer(row["Name"],row["Age"],ast.literal_eval(row["Borrowed books"]),"","")

		for row in Librarians_rows:
			librarian = Librarian(row["Name"],row["Age"],"","")


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
				user = Librarian(name,age,password,nickname)
				self.add_Librarian(user)
			else:
				user = Customer(name,age,[],password,nickname)
				self.add_Customer(user)
			print("REGISTRATION COMPLETED")
			print(f"Welcome, {name}!")


	def removeCustomer(self):
		print("Here are all the customers that our library has:")
		for customer in Customer.customers:
			print(customer)
		to_Remove = int(input("Input the ID of the customer that you want to remove: "))
		try:
			to_Remove = int(to_Remove)
		except(ValueError, TypeError):
			TypeError("ID does not contain symbols other than digits")
		for customer in Customer.customers:
			if customer.id == to_Remove:
				if len(customer.books_borrowed) == 0:
					Customer.customers.remove(customer)
					print(f"Customer {customer.name} has been removed")
				else:
					print("Sorry, you cannot remove this customer yet because he has not returned all the books he borrowed.")
			else:
				print("No Customer with such ID in the database")


	def add_Librarian(self,user):
		data = {"ID": [user.id], "Name": [user.name], "Age": [user.age]}
		df = pd.DataFrame(data)
		df.to_csv("Librarians_data.csv", mode="a", header=not os.path.exists("Librarians_data.csv"), index=False)
		data = {"ID": [user.id], "Nickname": [user.nickname], "Password": [user.password]}
		df = pd.DataFrame(data)
		df.to_csv("Librarians_nickname_pass.csv", mode="a", header=not os.path.exists("Librarians_nickname_pass.csv"), index=False)

	def add_Customer(self,user):
		data = {"ID": [user.id], "Name": [user.name], "Age": [user.age], "Borrowed books": [user.books_borrowed]}
		df = pd.DataFrame(data)
		df.to_csv("Customers_data.csv", mode="a", header=not os.path.exists("Customers_data.csv"), index=False)
		data = {"ID": [user.id], "Nickname": [user.nickname], "Password": [user.password]}
		df = pd.DataFrame(data)
		df.to_csv("Customers_nickname_pass.csv", mode="a", header=not os.path.exists("Customers_nickname_pass.csv"),
				  index=False)

	def add_book(self,book):
		data = {"title": [book.title], "publication_date": [book.publication_date], "authors": [book.authors],
				"genres": [book.genres], "borrowed": [book.borrowed]}
		df = pd.DataFrame(data)
		df.to_csv("filtered_books_library.csv", mode="a", header=not os.path.exists("filtered_books_library.csv"))

