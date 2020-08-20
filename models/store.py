"""Module that manages Store table"""
import mysql.connector as mc
from configuration import config as conf, sql_queries as sql


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
        """Method that connects MySQL server"""
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def disconnect(self):
        """Method that disconnects MySQL server"""
        self.cursor.close()
        self.cnx.close()

    def insert_store(self, store):

        self.connect()

        data_store = {'name': store.name}

        try:
            self.cursor.execute(sql.USE_DATABASE)
            self.cursor.execute(sql.INSERT_STORES, data_store)
            # id = cursor.lastrowid
            self.cnx.commit()

            # Récupérer id
            self.cursor.execute("SELECT LAST_INSERT_ID();")

            store.id = self.cursor.fetchone()[0]
            #print(f"Store ID: {store.id}")
            self.cnx.commit()

            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de l'insertion des lieux de vente. Détails de l'erreur: {err}")
