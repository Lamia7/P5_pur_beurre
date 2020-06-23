import mysql.connector as mc
import config as conf
import sql_queries


class Database:

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def create_database(self):
        """Create database"""

        cnx = self.cnx
        cursor = self.cursor
        try:
            cursor.execute(sql_queries.CREATE_SCHEMA)
            cursor.execute(sql_queries.USE_DATABASE)
            print("New schema successfully created.")
            cnx.commit()  # Commit/save changes on db

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful creation of a new schema: {err}")

    def create_tables(self):

        for table in sql_queries.TABLES:
            table_query = sql_queries.TABLES[table]
            try:
                self.connect()
                cnx = self.cnx
                cursor = self.cursor
                cursor.execute(sql_queries.USE_DATABASE)
                cursor.execute(table_query)
                print(f"Table {table} successfully created.")
                cnx.commit()  # Commit/save changes on db

                cursor.close()
                cnx.close()
            except mc.Error as err:
                print(f"Unsuccessful creation of table named {table}, due to error: {err}")


db = Database()
db.create_database()
db.create_tables()
