import mysql.connector as mc
import config as conf


class Database:

    def __init__(self, user=conf.USER,
                 password=conf.PASSWORD,
                 host=conf.HOST,
                 database_name=conf.DATABASE_NAME
                 ):
        self.user = user
        self.password = password
        self.host = host
        self.database_name = database_name

    def connect(self):
        """Connect to MySQL server"""
        try:
            cnx = mc.connect(self.user, self.password, self.host, self.database_name)
            print("Connection successful.")
            cnx.close()
        except mc.Error as err:
            print(f"Connection unsuccessful : {err}")
