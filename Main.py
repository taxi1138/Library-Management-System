from Menu.Menu import Menu
import pandas as pd
import os

df = pd.read_csv("filtered_books.csv")
df["publication_date"] = df["publication_date"].fillna("00/00/00")
df.to_csv("filtered_books.csv",mode= "a",header=not os.path.exists("filtered_books.csv"))
menu = Menu()
menu.load_data()
menu.login()
menu.searchByGenre()
menu.assign_book()

