class Book:
	storage = []
	def __init__(self,title,authors,publication_date,rating,genres,borrowed):
		self.title = title
		self.publication_date = publication_date
		self.rating = rating
		self.authors = []
		self.genres = []
		self.borrowed = False
		Book.storage.append(self)





