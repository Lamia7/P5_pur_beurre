from downloader import Downloader
from database import Database
from models.product import ProductManager
from models.category import CategoryManager
from models.store import StoreManager

# Get cleaned data
download = Downloader()
download.avoid_empty()
download.get_products()

downloaded_products = download.final_products  # returns list of objects of final downloaded products

# Create database with empty tables
db = Database()
db.create_database()
db.create_tables()

# Insert each product to database
pm = ProductManager()
for one_product in downloaded_products:
    pm.insert_product(one_product)
print("Products inserted to database.")

# Insert each category to database
cm = CategoryManager()
for one_product in downloaded_products:
    cm.insert_category(one_product)
print("Categories inserted to database.")

# Insert each store to database
sm = StoreManager()
for one_product in downloaded_products:
    sm.insert_store(one_product)
print("Stores inserted to database.")
