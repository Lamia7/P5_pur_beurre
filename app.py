"""Main file that runs the app"""
from menus.menu import Menu
from product_management.main import init_database

if __name__ == '__main__':
    init_database()
    menu = Menu()
    menu.display_menu()
