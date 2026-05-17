class Person:
	def __init__(self, name, age):
		self.set_name(name)
		self.set_age(age)


	def get_info(self):
		return f"arbitrary person of Name:{self.name} and Age:{self.age}"


	def set_name(self,name):
		if not isinstance(name, str):
			raise TypeError("Name must be of String type!")
		if len(name.strip())<1:
			raise ValueError("Name cannot be left empty!")
		if not name.replace(" ","").isalpha():
			raise ValueError("Name must contain letters and nothing else!")
		self.name = name


	def set_age(self,age):
		try:
			age = int(age)
		except:
			raise TypeError("Age must be of type Integer!")
		if age<0:
			raise ValueError("Age cannot be negative!")
		self.age = age

	#def verify_nickname(self,nickname):
	#	while not isinstance(nickname, str):
	#		print("nickname can include special symbols and digits, but it must be of type String!")
	#		print("Maybe your nickname is already taken be someone.")
	#		print("Try again.", end = " ")
	#		nickname = input("New nickname: ")
	#	self.nickname = nickname
#
#	def verify_password(self,password):
#		while not isinstance(password, str) or len(password) < 6:
#			print("Password must be of String type and contain at least 6 symbols!")
#			print("Try again", end = " ")
#			password = input("New password: ")
#		self.password = password