import pandas as pd
import os
from classes.Person import Person
from random import randint


class Customer(Person):
	login_pass_Customer = {}
	customers = []
	customer_id = set()
	test_id = ""

	def __init__(self,id,name,age,books_borrowed,password,nickname):
		super().__init__(name,age)
		if id == "":
			while True:
				self.test_id = ""
				for i in range(10):
					self.test_id += str(randint(0, 9))
				if self.test_id not in self.customer_id:
					break
			self.id = self.test_id
			self.test_id = ""
		else:
			self.id = id
		self.customer_id.add(self.id)
		self.books_borrowed = books_borrowed
		self.verify_nickname(nickname)
		self.verify_password(password)
		self.login_pass_Customer[f"{self.nickname}"] = self.password
		self.customers.append(self)


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

	def __str__(self):
		return f"ID: {self.id}, name: {self.name}, age: {self.age}"
