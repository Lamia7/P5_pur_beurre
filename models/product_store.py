import mysql.connector as mc
import config as conf
import sql_queries


class ProductStore:

    def __init__(self, product_id, store_id):
        self.product_id = product_id
        self.store_id = store_id

    def __str__(self):
        """String representation of ProductStore object"""
        return f"product_id: {self.product_id}, store_id: {self.store_id}"


class ProductStoreManager:
    """Manages store data"""

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def insert_product_and_store_ids(self, product_store_obj_list):
        cnx = self.cnx
        cursor = self.cursor
        self.connect()

        """Depuis une liste d'objets ProductStore
        Création d'une liste de dicos qui affecte l'id de product à product_id et
        l'id de store à store_id"""
        data_product_store_list = []
        for product_store_ob in product_store_obj_list:
            data_product_store_list.append(
                {'product_id': product_store_ob.product_id, 'store_id': product_store_ob.store_id})
        print(f"data_product_store_list: {data_product_store_list}")

        try:
            cursor.execute(sql_queries.USE_DATABASE)
            for prod_store_dict in data_product_store_list:
                cursor.execute(sql_queries.INSERT_PRODUCT_STORE, prod_store_dict)
                cnx.commit()

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful insertion of product_id and store_id: {err}")
