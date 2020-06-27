from downloader import Downloader
from database import Database
from models.product import ProductManager

# Get cleaned data
download = Downloader()
download.avoid_empty()
download.get_products()

downloaded_products = download.final_products  # returns list of objects of final downloaded products

# Create database with empty tables
db = Database()
db.create_database()
db.create_tables()

#
pm = ProductManager()

# Insert each product
for one_product in downloaded_products:
    pm.insert_product(one_product)
