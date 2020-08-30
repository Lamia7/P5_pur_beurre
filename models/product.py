"""Module that manages Product table"""
import mysql.connector as mc

from configuration import config as conf
from configuration import sql_queries as sql
from models.category import Category
from models.store import Store


class Product:
    """Class that creates products"""

    def __init__(self, clean_product):
        """Product description"""
        self.name = clean_product['product_name_fr']
        self.brands = clean_product['brands']
        self.barcode = clean_product['code']
        self.url = clean_product['url']
        self.nutriscore_grade = clean_product['nutriscore_grade']
        self.categories = []
        self.stores = []
        self.id = clean_product.get('id')
        self.set_categories(clean_product['categories'])  # cat to pdct dict
        self.set_stores(clean_product['stores'])

    def set_categories(self, clean_categories):
        """
        Method that creates a list of objects categories
        - for each category in categories list
        - instantiate a category object
        - adds each category object to the list
        no need to return as it is in self
        """
        self.categories = [Category(clean_category)
                           for clean_category in clean_categories]

    def set_stores(self, clean_stores):
        """
        Method that creates a list of objects stores
        - for each store in stores list
        - instantiate a store object
        - adds each store object to the list.
        """
        self.stores = [Store(clean_store) for clean_store in clean_stores]


class ProductManager:
    """Manages products data"""

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Method that connects MySQL server"""
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()
        return self.cursor, self.cnx

    def disconnect(self):
        """Method that disconnects MySQL server"""
        self.cursor.close()
        self.cnx.close()

    def insert_product(self, one_product):

        self.connect()

        # Creates a dict of data for insertion
        data_product = {'name': one_product.name,
                        'brands': one_product.brands,
                        'barcode': one_product.barcode,
                        'url': one_product.url,
                        'nutriscore_grade': one_product.nutriscore_grade
                        }

        try:
            # Insert products to product table
            self.cursor.execute(sql.USE_DATABASE)
            self.cursor.execute(sql.INSERT_PRODUCTS, data_product)
            self.cnx.commit()

            # Gets the product id auto incremented
            self.cursor.execute("SELECT LAST_INSERT_ID();")
            one_product.id = self.cursor.fetchone()[0]

            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de l'insertion des produits. "
                  f"Détails de l'erreur: {err}")
