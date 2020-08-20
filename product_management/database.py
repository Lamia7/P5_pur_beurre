import mysql.connector as mc
from configuration import config as conf, sql_queries


class Database:

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

    def create_database(self):
        """Create database"""

        self.connect()
        try:
            self.cursor.execute(sql_queries.CREATE_SCHEMA)
            self.cursor.execute(sql_queries.USE_DATABASE)
            #print(f"New database successfully created.\n"
                  #f"------------------------------------------------------")
            self.cnx.commit()  # Commit/save changes on db

            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de la mise à jour de la base de données. Détails de l'erreur: {err}")

    def create_tables(self):

        for table in sql_queries.TABLES:
            table_query = sql_queries.TABLES[table]
            try:
                self.connect()
                self.cursor.execute(sql_queries.USE_DATABASE)
                self.cursor.execute(table_query)
                #print(f"Table {table} successfully created.")
                self.cnx.commit()  # Commit/save changes on db

                self.disconnect()
            except mc.Error as err:
                print(f"Erreur lors de la mise à jour de la table '{table}'. Détails de l'erreur: {err}")