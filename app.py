from downloader import Downloader
from database import Database
from models.product import ProductManager
from models.category import CategoryManager
from models.product_category import ProductCategoryManager, ProductCategory
from models.store import StoreManager
from models.product_store import ProductStoreManager, ProductStore

# Get cleaned data
download = Downloader()
download.avoid_empty()
download.get_products()

downloaded_products = download.final_products  # returns list of objects of final downloaded products

# Create database with empty tables
db = Database()
db.create_database()
db.create_tables()

# ---------- Insert each product & category to database ---------- #
pm = ProductManager()
cm = CategoryManager()
sm = StoreManager()
# insert product
for one_product in downloaded_products:
    pm.insert_product(one_product)
    # insert category(ies)
    for category in one_product.categories:
        cm.insert_category(category)
    # insert store(s)
    for store in one_product.stores:
        sm.insert_store(store)
print("Products inserted to database.")
print("Categories inserted to database.")

# ---------- Insert product_id and category_id to product_category table ---------- #
# Creates a list of ProductCategory objects (ids)
product_category_obj_list = []
for product in downloaded_products:
    product_id = product.id  # id de l'objet product de la list
    for category in product.categories:
        category_id = category.id
        product_category_obj_list.append(ProductCategory(product_id, category_id))

# Creates a list of ProductStore objects (ids)
product_store_obj_list = []
for product in downloaded_products:
    product_id = product.id  # id de l'objet product de la list
    for store in product.stores:
        store_id = store.id
        product_store_obj_list.append(ProductStore(product_id, store_id))

pcm = ProductCategoryManager()
psm = ProductStoreManager()
pcm.insert_product_and_category_ids(product_category_obj_list)
print("Product_Category inserted to database.")
psm.insert_product_and_store_ids(product_store_obj_list)
print("Product_Store inserted to database.")

