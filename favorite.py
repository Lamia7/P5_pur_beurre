"""Module that manages Favorite table"""
import mysql.connector as mc
import sql_queries
import config as conf


class Favorite:
    """Class that creates favorites"""

    def __init__(self, name, nutriscore_grade, barcode, brands, url, store, id=None):
        """Favorite's description"""
        self.id = id
        self.name = name
        self.nutriscore_grade = nutriscore_grade
        self.barcode = barcode
        self.brands = brands
        self.url = url
        self.store = store

    def __str__(self):
        """String representation of Favorte object"""
        return f"----------------\n" \
               f"{self.id}" \
               f"{self.name}" \
               f"{self.nutriscore_grade}" \
               f"{self.barcode}" \
               f"{self.brands}" \
               f"{self.url}" \
               f"{self.store}" \



class FavoriteManager:
    """Manages Favorite data"""

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

    def insert_favorite(self, favorite):
        self.connect()

        data_favorite = {'name': favorite.name,
                         'nutriscore_grade': favorite.nutriscore_grade,
                         'barcode': favorite.barcode,
                         'brands': favorite.brands,
                         'url': favorite.url,
                         'store': favorite.store}

        try:
            # Insert substitute to favorite table
            self.cursor.execute(sql_queries.USE_DATABASE)
            self.cursor.execute(sql_queries.INSERT_FAVORITE, data_favorite)
            self.cnx.commit()

            # Gets the product id auto incremented
            self.cursor.execute("SELECT LAST_INSERT_ID();")
            favorite.id = self.cursor.fetchone()[0]
            self.cnx.commit()

            self.disconnect()
        except mc.Error as err:
            print(f"Unsuccessful insertion of favorite: {err}")
