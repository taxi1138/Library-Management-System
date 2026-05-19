

def decorator(func):
	def wrapper(self):
		if self.isLibrarian:
			func(self)
		else:
			print("Only Librarians have access to this function.")
	return wrapper
