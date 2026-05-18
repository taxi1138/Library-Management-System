from Menu.Menu_functions import Menu_functions
from classes.Customer import Customer
from classes.Librarian import Librarian
from classes.Book import Book
import pandas as pd
import os
import ast
from decorators.decorator import decorator,decorator_assign_book
import re

class Menu(Menu_functions):
	isLibrarian = False
	isCustomer = False
	user = None


	def load_data(self):
		Books_rows = pd.read_csv("filtered_books.csv",).to_dict(orient="records")
		customers_rows = pd.read_csv("Customers_data.csv").to_dict(orient = "records")
		Librarians_rows = pd.read_csv("Librarians_data.csv").to_dict(orient = "records")

		for row in Books_rows:
			Book(row["title"],ast.literal_eval(row["authors"]),row["publication_date"],ast.literal_eval(row["genres"]),row["borrowed"])

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
			login = input("Input nickname: ")
			password = input("Input password: ")
			if self.isLibrarian:
				if login in Librarian.login_pass_Librarian.keys():
					if Librarian.login_pass_Librarian[login] == password:
						for librarian in Librarian.Librarians:
							if librarian.nickname == login:
								self.user = librarian
								print("Welcome back, Librarian!")
								break
						return
					else:
						raise ValueError("Invalid nickname or password!")
				else:
					raise ValueError("There is no Librarian with such nickname in the database")
			else:
				if login in Customer.login_pass_Customer.keys():
					if Customer.login_pass_Customer[login] == password:
						for customer in Customer.customers:
							if customer.nickname == login:
								self.user = customer
								print("Welcome back, Customer!")
								break
						return
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
				self.user = Librarian("",name,age,password,nickname)
				self.save_Librarian(self.user)
			else:
				self.user = Customer("",name,age,[],password,nickname)
				self.save_Customer(self.user)
			print("REGISTRATION COMPLETED")
			print(f"Welcome, {name}!")


	@decorator_assign_book
	def assign_book(self,book,user):
		if book not in user.books_borrowed:
			if book.borrowed == 0:
				if self.isCustomer:
					book.borrowed = 1
					user.books_borrowed.append(book)
					print(f"The book {book.title} is now yours, but dont forget to return it.")
					return
				else:
					print(f"You don't have to ask, Librarian. The book {book.title} is yours.")
					return
			else:
				print(f"Sorry, you cannot borrow this book, someone has already taken it.")
				return
		else:
			return "The book is already yours, no need to try to borrow it twice."



	def return_book(self,book,user):
		if book in user.books_borrowed:
			book.borrowed = 0
			user.books_borrowed.remove(book)
			print(f"You returned the book {book.title}.")
		else:
			print(f"You cannot return the book {book.title} since you never borrowed it.")


	def search_by_genre(self):
		decision = input("Are you looking for books with single genre or multiple genres? (single/mult): ")
		if decision.lower() == "single":
			genre = input("Input the genre you are looking for(First letters must be capital): ")
			print(f"These are the books with the genre {genre}:")
			for book in Book.storage:
				if genre in book.genres:
					print(book)
			book_title = input("Input the title of the book you liked: ")
			if book_title == "":
				print("No book was given to you because you didn't input title.")
				return
			else:
				for book in Book.storage:
					if book.title.lower() == book_title.lower():
						if not self.isLibrarian:
							self.isLibrarian = True
							self.assign_book(book,self.user)
							self.isLibrarian = False
						else:
							self.assign_book(book,self.user)
						return
		elif decision.lower() == "mult":
			genres = []
			genres_num = int(input("Input how many genres you are looking for: "))
			for i in range(genres_num):
				genre = input(f"Input genre {i}: ")
				genres.append(genre)
			for book in Book.storage:
				for genre_ in genres:
					if genre_ not in book.genres:
						continue
				print(book)
			book_title = input("Input the title of the book you liked(leave empty if didn't like any): ")
			if book_title == "":
				print("No book was given to you because you didn't input title")
				return
			else:
				for book in Book.storage:
					if book.title.lower() == book_title.lower():
						if not self.isLibrarian:
							self.isLibrarian = True
							self.assign_book(book,self.user)
							self.isLibrarian = False
						else:
							self.assign_book(book,self.user)
						return



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
		book = Book(title, authors, date, genres, 0)
		self.save_book(book)
		print(f"The book {title} was added to the database.")


	def advanced_search(self):
		author = ""
		year_begin = ""
		year_end = ""
		genre = ""
		genres = []
		exclude_genre = ""
		exclude_genres = []
		author = input("Input the author you search for (leave empty if no need): ")
		pattern_year = r"^\d{2}$"
		year_begin = input("Input the lower bound for search by year of publication(leave empty if no need). Form of input must be YY: ")
		if year_begin!="":
			if not re.match(pattern_year, year_begin):
				print("Invalid input. Form of input for years must be YY")
				return
		if year_begin == "":
			year_end = ""
		else:
			year_end = input("Input the upper bound for search by year of publication(cannot be left empty, since year_begin != '').Form of input must be YY: ")
			if not re.match(pattern_year,year_end):
				print("Invalid input. Form of input for years must be YY")
				return
			if int(year_end) < int(year_begin):
				print("First input of year must be smaller since we will check for books that fit in the range from year_begin to year_end.")
				return
		choice = input("Do you want to search by single or multiple genres?(leave empty if no need): ")
		if choice != "":
			if choice.lower() == "single":
				genre = input("Input the genre you are searching for (must start with capital letter): ")
			elif choice.lower() == "mult":
				genres_num = int(input("How many genres will you search for?: "))
				for i in range(genres_num):
					genre = input(f"Input genre {i} (must start with capital letter): ")
					genres.append(genre)
			else:
				print("Invalid input")
				return
		choice = input("Do you want to exclude single or multiple genres?(leave empty if no need): ")
		if choice !="":
			if choice.lower() == "single":
				exclude_genre = input("Input the genre you want to exclude(must start with capital letter): ")
				if exclude_genre == genre:
					print("You cannot exclude genre that you are searching for.")
					return
			elif choice.lower() == "mult":
				exclude_genres_num = int(input("Input how many genres you want to exclude: "))
				for i in range(exclude_genres_num):
					exclude_genre = input(f"Input exclude_genre {i} (must start with capital letter): ")
					exclude_genres.append(exclude_genre)
					if exclude_genre in genres:
						print("You cannot exclude genres you are searching for.")
						return
			else:
				print("Invalid input.")
				return

		valid_books = set()
		for book in Book.storage:
			if self.author_check(author,book) and self.genres_check(genre,genres,book) and self.date_check(year_begin,year_end,book) and self.exclude_genres_check(exclude_genre,exclude_genres,book):
				print(book)
				valid_books.add(book)
		title = input("Input the title of the book you liked(leave empty if not interested): ")
		if title == "":
			print("No book has been given to you because you didn't input title.")
			return
		for book in valid_books:
			if book.title.lower() == title.lower():
				if book.borrowed!=1:
					if isinstance(self.user,Customer):
						book.borrowed = 1
						self.user.books_borrowed.append(book)
						print(f"You just borrowed the book '{book.title}'. Do not forget to return it.")
						return
					else:
						print("You may borrow the book, Librarian")
						return
				else:
					print("Sorry, this book has already been taken by someone. You cannot borrow it.")
					return


	def author_check(self,author,book):
		if author == "":
			return True
		else:
			for author_ in book.authors:
				if author_.lower() == author.lower():
					return True
			return False

	def genres_check(self,genre,genres, book):
		if len(genres)==0 and genre == "":
			return True
		else:
			if genre != "":
				if genre in book.genres:
					return True
				else:
					return False
			elif len(genres)!=0:
				for genre_ in genres:
					if genre_ not in book.genres:
						return False
					else:
						continue
				return True

	def date_check(self,year_begin,year_end, book):
		if year_begin == "":
			return True
		else:
			int_year_begin = int(year_begin)
			int_year_end = int(year_end)
			date =  int(book.publication_date[-2:])
			if int_year_begin <= date <= int_year_end:
				return True
			else:
				return False

	def exclude_genres_check(self,exclude_genre, exclude_genres,book):
		if len(exclude_genres)==0 and exclude_genre == "":
			return True
		else:
			if exclude_genre!="":
				if exclude_genre not in book.genres:
					return True
				else:
					return False
			if len(exclude_genres)!=0:
				for genre in exclude_genres:
					if genre in book.genres:
						return False
				return True


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
		df.to_csv("filtered_books1.csv", mode="a", header=not os.path.exists("filtered_books.csv"))



