from classes.Customer import Customer
from classes.Person import Person
from classes.Book import Book
from random import randint
import pandas as pd
import os


class Librarian(Person):
	login_pass_Librarian = {}
	Librarians = []
	librarian_ID = set()
	test_id = ""

	def __init__(self,id,name,age,password,nickname):
		super().__init__(name,age)
		if id == "":
			while True:
				self.test_id = ""
				for i in range(10):
					self.test_id += str(randint(0, 9))
				if self.test_id not in self.librarian_ID:
					break
			self.id = self.test_id
			self.test_id = ""
		else:
			self.id = id
		self.librarian_ID.add(self.id)
		if self.age < 18:
			raise ValueError("You cannot become a Librarian before you turn 18!")
		self.verify_password(password)
		self.verify_nickname(nickname)
		self.login_pass_Librarian[f"{self.nickname}"] = self.password
		self.Librarians.append(self)


	def get_info(self):
		return f"A Librarian of Name:{self.name} and Age:{self.age}"


	def verify_nickname(self,nickname):
		while (not isinstance(nickname, str)) or (nickname in self.login_pass_Librarian.keys()):
			print("nickname can include special symbols and digits, but it must be of type String!")
			print("Maybe your nickname has already been taken by someone.")
			print("Try again.", end = " ")
			nickname = input("New nickname: ")
		self.nickname = nickname

	def verify_password(self,password):
		while True:
			try:
				if not isinstance(password, str):
					raise TypeError("Password must be a string")
				if len(password) < 6:
					raise ValueError("Password must be at least 6 characters long")
				self.password = password
				break
			except (TypeError, ValueError) as e:
				print(e)
				print("Try again.")
				password = input("New password: ")

