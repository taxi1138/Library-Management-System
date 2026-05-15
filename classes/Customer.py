from classes.Person import Person


class Customer(Person):
	login_pass_Customer = {}

	def __init__(self,name,age,books_borrowed,password,nickname):
		super().__init__(name,age)
		self.books_borrowed = []
		self.verify_nickname(nickname)
		self.verify_password(password)
		self.login_pass_Customer[f"{self.nickname}"] = self.password

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