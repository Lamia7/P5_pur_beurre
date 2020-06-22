import mysql.connector as mc
import config as conf
import sql_queries


kwargs = {'user': conf.USER, 'password': conf.PASSWORD, 'host': conf.HOST, 'database': None}  # None or '' ?


class Database:

    def __init__(self):
        self.create_database()

    @staticmethod
    def create_database():
        """Create database"""

        try:
            cnx = mc.connect(**kwargs)
            cursor = cnx.cursor()  # init cursor

            cursor.execute(sql_queries.CREATE_SCHEMA)
            cursor.execute(sql_queries.USE_DATABASE)
            print("New schema successfully created.")
            cnx.commit()  # Commit/save changes on db

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful creation of a new schema: {err}")

    @staticmethod
    def create_tables():

        for table in sql_queries.TABLES:
            table_query = sql_queries.TABLES[table]
            try:
                cnx = mc.connect(**kwargs)
                cursor = cnx.cursor()  # init cursor

                cursor.execute(sql_queries.USE_DATABASE)
                cursor.execute(table_query)
                print(f"Table {table} successfully created.")
                cnx.commit()  # Commit/save changes on db

                cursor.close()
                cnx.close()
            except mc.Error as err:
                print(f"Unsuccessful creation of table named {table}, due to error: {err}")


db = Database()
db.create_tables()
