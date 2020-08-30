"""Module that manages Store table"""
import mysql.connector as mc

from configuration import config as conf
from configuration import sql_queries as sql


class Store:

    def __init__(self, name, id=None):
        """Store description"""
        self.id = id
        self.name = name


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
            self.cnx.commit()

            # Get id
            self.cursor.execute("SELECT LAST_INSERT_ID();")

            store.id = self.cursor.fetchone()[0]
            self.cnx.commit()

            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de l'insertion des lieux de vente. "
                  f"Détails de l'erreur: {err}")
