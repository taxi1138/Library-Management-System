from Menu.Menu_functions import Menu_functions
from classes.Customer import Customer
from classes.Librarian import Librarian
from classes.Book import Book
import pandas as pd
import ast
from decorators.decorator import decorator
import re

class Menu(Menu_functions):
	isLibrarian = False
	isCustomer = False
	user = None

	def run_interface(self):
		running = True
		while running:
			print("\n===== LIBRARY MENU =====")
			print("1. Login / Register")
			print("2. Search by genre")
			print("3. Search by author")
			print("4. Advanced search")
			print("5. Add book")
			print("6. Show all customers")
			print("7. Show all librarians")
			print("8. Return book")
			print("0. Exit")
			choice = input("Input your choice: ")
			match choice:
				case "1":
					self.login()
				case "2":
					if self.require_login():
						self.search_by_genre()
				case "3":
					if self.require_login():
						self.search_by_author()
				case "4":
					if self.require_login():
						self.advanced_search()
				case "5":
					if self.require_login():
						self.add_book()
				case "6":
					if self.require_login():
						self.show_customers()
				case "7":
					if self.require_login():
						self.show_librarians()
				case "8":
					if self.require_login():
						self.return_book()
				case "0":
					print("Goodbye!")
					self.save_data()
					running = False
				case _:
					print("Invalid choice!")
			if running:
				input("\nPress Enter to continue...")


	def require_login(self):
		if self.user is None:
			print("You must login or register first!")
			return False
		return True


	def load_data(self):
		Books_rows = pd.read_csv("filtered_books.csv",).to_dict(orient="records")
		customers_rows = pd.read_csv("Customers_data.csv").to_dict(orient = "records")
		Librarians_rows = pd.read_csv("Librarians_data.csv").to_dict(orient = "records")

		for row in Books_rows:
			Book(row["title"],ast.literal_eval(row["authors"]),row["publication_date"],ast.literal_eval(row["genres"]),row["borrowed"])

		for row in customers_rows:
			val = row["Borrowed books"]
			if pd.isna(val) or str(val).strip() in ["", "[]", "nan"]:
				val = ""
			else:
				val = str(val).strip()
			Customer(row["ID"],row["Name"],row["Age"],val,row["Password"],row["Nickname"])

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
			else:
				self.user = Customer("",name,age,"",password,nickname)
			print("REGISTRATION COMPLETED")
			print(f"Welcome, {name}!")


	def assign_book(self,book,user):
		is_borrowed = True
		if self.isCustomer:
			if user.books_borrowed == "" or user.books_borrowed == []:
				is_borrowed = True
			else:
				print("you cannot borrow more than one book at a time.")
				return

		if is_borrowed:
			if book.borrowed == 0:
				if self.isCustomer:
					book.borrowed = 1
					user.books_borrowed = book.title
					print(f"The book {book.title} is now yours, but dont forget to return it.")
					return
				else:
					print(f"You don't have to ask, Librarian. The book {book.title} is yours.")
					return
			else:
				print(f"Sorry, you cannot borrow this book, someone has already taken it.")
				return

	def return_book(self):
		borrowed = str(self.user.books_borrowed).strip()
		if not borrowed or borrowed == "nan":
			print("You have no books to return.")
			return

		print(f"You currently have: {borrowed}")
		title = input("Input the title of the book you want to return: ").strip()
		if title == "":
			print("No title entered.")
			return
		if borrowed.lower() != title.lower():
			print("You did not borrow this book.")
			return

		for book in Book.storage:
			if book.title.lower() == title.lower():
				book.borrowed = 0
				break
		else:
			print("Book not found in library database.")
			return
		self.user.books_borrowed = ""
		print(f"You have successfully returned '{title}'.")


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
						self.assign_book(book, self.user)
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
		Book(title, authors, date, genres, 0)
		print(f"The book {title} was added to the database.")


	def advanced_search(self):
		year_begin = ""
		year_end = ""
		genre = ""
		genres = []
		exclude_genre = ""
		exclude_genres = []
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

		valid_books = []
		for book in Book.storage:
			if self.genres_check(genre,genres,book) and self.date_check(year_begin,year_end,book) and self.exclude_genres_check(exclude_genre,exclude_genres,book):
				print(book)
				valid_books.append(book)
		title = input("Input the title of the book you liked(leave empty if not interested): ")
		if title == "":
			print("No book has been given to you because you didn't input title.")
			return
		for book in valid_books:
			if book.title.lower() == title.lower():
				self.assign_book(book,self.user)
				return



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


	def search_by_author(self):
		for book in Book.storage:
			print(book.authors)
		author = input("Input the name of the author you want to search(make sure his name is written right): ").lower()
		if author == "":
			print("We didn't search for author because you didn't input the name of one.")
			return
		else:
			for book in Book.storage:
				authors = [x.lower() for x in book.authors]
				if any(author in a for a in authors):
					print(book)
			book_title = input("Input the title of the book you liked: ")
			if book_title == "":
				print("No book was given to you because you didn't input title")
				return
			else:
				for book in Book.storage:
					if book.title.lower() == book_title.lower():
						self.assign_book(book, self.user)
						return


	@decorator
	def show_customers(self):
		for customer in Customer.customers:
			print(customer.get_info())

	@decorator
	def show_librarians(self):
		for librarian in Librarian.Librarians:
			print(librarian.get_info())


	def save_data(self):
		data = []
		for book in Book.storage:
			row = {"title": book.title, "publication_date": book.publication_date, "authors": book.authors, "genres": book.genres, "borrowed": book.borrowed}
			data.append(row)
		df_books = pd.DataFrame(data)
		df_books.to_csv("filtered_books.csv", index = False)

		data = []
		for customer in Customer.customers:
			row = {"ID": customer.id, "Name": customer.name, "Age": customer.age, "Borrowed books": customer.books_borrowed, "Nickname":customer.nickname, "Password":customer.password}
			data.append(row)
		df_customers = pd.DataFrame(data)
		df_customers.to_csv("Customers_data.csv", index = False)

		data = []
		for librarian in Librarian.Librarians:
			row = {"ID": librarian.id, "Name": librarian.name, "Age": librarian.age, "Nickname": librarian.nickname,"Password": librarian.password}
			data.append(row)
		df_librarians = pd.DataFrame(data)
		df_librarians.to_csv("Librarians_data.csv", index = False)







