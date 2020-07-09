"""Module that manages Product table"""
import mysql.connector as mc
import sql_queries
import config as conf
from models.category import Category


class Product:
    """Class that creates products"""

    def __init__(self, raw_product):
        """description d'un produit: il a un nom, des catégories, marque, magasins, code, ingrédients, url, nutriscore"""
        self.name = raw_product['product_name_fr']
        self.brands = raw_product['brands']
        self.barcode = raw_product['code']
        self.url = raw_product['url']
        self.nutriscore_grade = raw_product['nutriscore_grade']
        self.categories = []
        self.set_categories(raw_product['categories'])  # envoie categories du dico product à la méthode

    def __str__(self):
        """String representation of Product object"""
        return f"----------------\n" \
               f"{self.name} {self.brands} {self.barcode}" \
               f"{self.categories}" \
               f"{self.url}" \
               f"{self.nutriscore_grade}"

    def set_categories(self, raw_categories):
        """Crée une liste d'objets categories
        - pour chaque cat de la liste categories
        - instancie un objet category
        - ajoute chaque objet à la liste
        pas besoin de le return car self."""
        self.categories = [Category(raw_category) for raw_category in raw_categories]


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

        data_product = {'name': one_product.name,
                        'brands': one_product.brands,
                        'barcode': one_product.barcode,
                        'url': one_product.url,
                        'nutriscore_grade': one_product.nutriscore_grade
                        }

        try:
            cursor.execute(sql_queries.USE_DATABASE)
            cursor.execute(sql_queries.INSERT_PRODUCTS, data_product)
            # product_id = cursor.lastrowid
            cnx.commit()

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful insertion of products: {err}")

    def display_product(self):
        pass
