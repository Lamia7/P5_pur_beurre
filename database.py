import mysql.connector as mc
import config as conf
import sql_queries


kwargs = {'user': conf.USER, 'password': conf.PASSWORD, 'host': conf.HOST, 'database': ''}


class Database:

    def __init__(self):
        self.create_database()

    @staticmethod
    def create_database():
        """Create database"""

        try:
            cnx = mc.connect(**kwargs)
            cursor = cnx.cursor()  # init cursor

            # Create database
            cursor.execute(sql_queries.CREATE_SCHEMA)
            cursor.execute(sql_queries.USE_DATABASE)
            print("New schema successfully created.")
            cnx.commit()  # Commit/save changes on db

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful creation of a new schema: {err}")


db = Database()
