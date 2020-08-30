"""Module that manages ProductStore table"""
import mysql.connector as mc

from configuration import config as conf
from configuration import sql_queries as sql


class ProductStore:

    def __init__(self, product_id, store_id):
        """ProductStore description"""
        self.product_id = product_id
        self.store_id = store_id


class ProductStoreManager:
    """Manages store data"""

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

    def insert_product_and_store_ids(self, product_store_obj_list):
        """From a list of objects ProductStore (product_store_obj_list),
        method creates a list of dict that affects id product to 'product_id'
        and id store to 'store_id'
        """

        self.connect()

        data_product_store_list = []
        for product_store_ob in product_store_obj_list:
            data_product_store_list.append(
                {'product_id': product_store_ob.product_id,
                 'store_id': product_store_ob.store_id})

        try:
            self.cursor.execute(sql.USE_DATABASE)
            for prod_store_dict in data_product_store_list:
                self.cursor.execute(sql.INSERT_PRODUCT_STORE, prod_store_dict)
                self.cnx.commit()

            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de l'insertion de product_id et store_id. "
                  f"Détails de l'erreur: {err}")
