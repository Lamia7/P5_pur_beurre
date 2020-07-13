"""Module that manages Category table"""
import mysql.connector as mc
import config as conf
import sql_queries


class Category:

    def __init__(self, name, id=None):
        self.name = name
        self.id = id

    def __str__(self):
        return f"{self.name}, {self.id}"


class CategoryManager:
    """Manages category data"""

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def insert_category(self, category):
        cnx = self.cnx
        cursor = self.cursor
        self.connect()

        data_category = {'name': category.name}

        try:
            # Insert categories to category table
            cursor.execute(sql_queries.USE_DATABASE)
            cursor.execute(sql_queries.INSERT_CATEGORIES, data_category)
            cnx.commit()

            # Gets the id auto incremented
            cursor.execute("SELECT LAST_INSERT_ID();")
            category.id = cursor.fetchone()[0]
            print(f"ID category: {category.id}")

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful insertion of categories: {err}")

    def display_category(self):
        pass
