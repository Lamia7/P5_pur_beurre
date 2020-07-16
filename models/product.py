"""Module that manages Product table"""
import mysql.connector as mc
import sql_queries
import config as conf
from models.category import Category
from models.store import Store


class Product:
    """Class that creates products"""

    def __init__(self, clean_product):
        """description d'un produit: il a un nom, des catégories, marque, magasins, code, ingrédients, url, nutriscore"""
        self.name = clean_product['product_name_fr']
        self.brands = clean_product['brands']
        self.barcode = clean_product['code']
        self.url = clean_product['url']
        self.nutriscore_grade = clean_product['nutriscore_grade']
        self.categories = []
        self.stores = []
        self.id = clean_product.get('id')
        self.set_categories(clean_product['categories'])  # sends categories to product dict into set_categories()
        self.set_stores(clean_product['stores'])

    def __str__(self):
        """String representation of Product object"""
        return f"----------------\n" \
               f"{self.name} {self.brands} {self.barcode}" \
               f"{self.categories}" \
               f"{self.url}" \
               f"{self.nutriscore_grade}"

    def set_categories(self, clean_categories):
        """
        Method that creates a list of objects categories
        - for each category in categories list
        - instantiate a category object
        - adds each category object to the list
        no need to return as it is in self
        """
        self.categories = [Category(clean_category) for clean_category in clean_categories]

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
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def insert_product(self, one_product):

        cnx = self.cnx
        cursor = self.cursor
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
            cursor.execute(sql_queries.USE_DATABASE)
            cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
            cnx.commit()

            # Gets the product id auto incremented
            cursor.execute("SELECT LAST_INSERT_ID();")
            one_product.id = cursor.fetchone()[0]
            # ou : one_product.id = cursor.lastrowid sans ligne 87,88
            print(f"ID product: {one_product.id}")
            #cnx.commit()

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful insertion of products: {err}")

    def display_product(self):
        pass
