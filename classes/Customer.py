from classes.Person import Person


class Customer(Person):
	def __init__(self,name,age,books_borrowed,password,nickname):
		super().__init__(name,age,nickname,password)
		self.books_borrowed = []

	def get_info(self):
		return f"A Customer of Name:{self.name} and Age:{self.age}"