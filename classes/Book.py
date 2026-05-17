import pandas as pd
import os

from pandas import DataFrame


class Book:
	storage = []
	def __init__(self,title,authors,publication_date,genres,borrowed):
		self.title = title
		self.publication_date = publication_date
		self.authors = []
		self.genres = []
		self.borrowed = False
		Book.storage.append(self)







