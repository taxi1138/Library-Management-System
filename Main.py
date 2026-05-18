from Menu.Menu import Menu
import pandas as pd
import os


menu = Menu()
menu.load_data()
menu.login()
menu.search_by_genre()
menu.advanced_search()
