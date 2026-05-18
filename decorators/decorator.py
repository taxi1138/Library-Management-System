

def decorator(func):
	def wrapper(self):
		if self.isLibrarian:
			func(self)
		else:
			print("Only Librarians have access to this function.")
	return wrapper

def decorator_assign_book(func):
	def wrapper(self,book,user):
		if self.isLibrarian:
			func(self,book,user)
		else:
			print("Only Librarians have access to this function.")
	return wrapper
