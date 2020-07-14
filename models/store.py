"""Module that manages Store table"""
import mysql.connector as mc
import config as conf
import sql_queries


class Store:

    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    def __str__(self):
        return f"{self.name}, {self.id}"


class StoreManager:
    """Manages category data"""

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def insert_store(self, store):
        cnx = self.cnx
        cursor = self.cursor
        self.connect()

        data_store = {'name': store.name}

        try:
            cursor.execute(sql_queries.USE_DATABASE)
            cursor.execute(sql_queries.INSERT_STORES, data_store)
            # id = cursor.lastrowid
            cnx.commit()

            # Récupérer id
            cursor.execute("SELECT LAST_INSERT_ID();")

            store.id = cursor.fetchone()[0]
            print(f"Store ID: {store.id}")
            cnx.commit()

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful insertion of stores: {err}")

    def display_category(self):
        pass

