import re
import regex

class Book:
	storage = []
	def __init__(self,title,authors,publication_date,genres,borrowed):
		self.set_title(title)
		self.set_date(publication_date)
		self.set_authors(authors)
		self.set_genres(genres)
		self.borrowed = borrowed
		Book.storage.append(self)

	def __str__(self):
		return f"Title: {self.title}, authors: {self.authors}, date: {self.publication_date}, genres: {self.genres}"

	def set_authors(self, authors):
		if not isinstance(authors, list):
			raise TypeError("authors must be a list")
		cleaned_authors = []
		for author in authors:
			if not isinstance(author, str):
				raise TypeError("names of the authors must be of String type")
			author = author.strip()
			if len(author) == 0:
				raise ValueError("Name of author must be mentioned")
			letters_only = regex.sub(r'[^\p{L}]', '', author)
			if len(letters_only) == 0:
				continue
			cleaned_authors.append(author)
		self.authors = cleaned_authors


	def set_genres(self, genres):
		for genre in genres:
			if not isinstance(genre, str):
				raise TypeError("all genres must be of String type")
			if len(genre) == 0:
				raise ValueError("Genres must be mentioned and no empty spaces must be left behind")
		self.genres = genres


	def set_title(self, title):
		if not isinstance(title, str):
			raise TypeError("Title must be of String type")
		if len(title)==0:
			raise ValueError("Title cannot be left empty")
		self.title = title

	def set_date(self,publication_date):
		if not isinstance(publication_date, str):
			print(publication_date)
			raise TypeError("Publication date must be of type string")
		if len(publication_date)==0:
			raise ValueError("Publication date cannot be left empty")
		publication_date = str(publication_date).strip()
		pattern = r"^(0[1-9]|1[0-2])/([0-2][0-9]|3[01])/\d{2}$"
		if not re.match(pattern, publication_date):
			print(publication_date)
			raise ValueError("Publication date must be of format MM/DD/YY")
		self.publication_date = publication_date






