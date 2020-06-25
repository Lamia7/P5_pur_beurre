from downloader import Downloader
from database import Database

# Get cleaned data
download = Downloader()
download.avoid_empty()
download.get_products()

# Create database with empty tables
db = Database()
db.create_database()
db.create_tables()
