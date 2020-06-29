import mysql.connector as mc
import sql_queries
import config as conf


class Product:
    """Class that creates products"""

    def __init__(self,
                 name,
                 category,
                 brands,
                 barcode,
                 store,
                 url,
                 nutriscore_grade
                 ):
        """description d'un produit: il a un nom, des catégories, marque, magasins, code, ingrédients, url, nutriscore"""
        self.name = name
        self.category = category
        self.brands = brands
        self.barcode = barcode
        self.store = store
        self.url = url
        self.nutriscore_grade = nutriscore_grade

    def __str__(self):
        """String representation of Product object"""
        return f"----------------\n" \
               f"{self.name} {self.brands} {self.barcode}" \
               f"{self.category}" \
               f"{self.store}" \
               f"{self.url}" \
               f"{self.nutriscore_grade}"


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

        data_product = (one_product.name,
                        one_product.brands,
                        one_product.barcode,
                        one_product.url,
                        one_product.nutriscore_grade
                        )

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
