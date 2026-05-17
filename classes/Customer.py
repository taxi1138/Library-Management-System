import pandas as pd
import os
from classes.Person import Person


class Customer(Person):
	login_pass_Customer = {}
	customers = []
	customer_id = 0

	def __init__(self,name,age,books_borrowed,password,nickname):
		self.id = self.customer_id
		super().__init__(name,age)
		self.books_borrowed = []
		self.verify_nickname(nickname)
		self.verify_password(password)
		self.login_pass_Customer[f"{self.nickname}"] = self.password
		self.customers.append(self)
		self.customer_id += 1


	def get_info(self):
		return f"A Customer of Name:{self.name} and Age:{self.age}"

	def verify_nickname(self, nickname):
		while (not isinstance(nickname, str)) or (nickname in self.login_pass_Customer.keys()):
			print("Nickname must be of type String!")
			print("Maybe your nickname has already been taken by someone.")
			print("Try again.", end = " ")
			nickname = input("New nickname: ")
		self.nickname = nickname

	def verify_password(self, password):
		while (not isinstance(password, str)) or (len(password)<6):
			print("Password must be of type String and at least 6 symbols in length.")
			print("Try again.")
			password = input("New password: ")
		self.password = password

	def __str__(self):
		return f"ID: {self.id}, name: {self.name}, age: {self.age}"
