"""Module that manages Category table"""
import mysql.connector as mc

from configuration import config as conf
from configuration import sql_queries


class Category:

    def __init__(self, name, id=None):
        """Category description"""
        self.name = name
        self.id = id


class CategoryManager:
    """Manages category data"""

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Method that connects MySQL server"""
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def disconnect(self):
        """Method that disconnects MySQL server"""
        self.cursor.close()
        self.cnx.close()

    def insert_category(self, category):

        self.connect()

        # Creates a dict of data for insertion
        data_category = {'name': category.name}

        try:
            # Insert categories to category table
            self.cursor.execute(sql_queries.USE_DATABASE)
            self.cursor.execute(sql_queries.INSERT_CATEGORIES, data_category)
            self.cnx.commit()

            # Gets the id auto incremented
            self.cursor.execute("SELECT LAST_INSERT_ID();")
            category.id = self.cursor.fetchone()[0]
            self.cnx.commit()

            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de l'insertion des catégories. "
                  f"Détails de l'erreur: {err}")
