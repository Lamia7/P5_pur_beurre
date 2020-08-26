"""Configuration file for optimization of other files"""

# ---------- DATABASE/USER CONFIGURATION ---------- #
USER = 'root'
PASSWORD = 'lamia'
HOST = 'localhost'
DATABASE_NAME = 'DataFood'

MYSQLCONFIG = {'user': USER,
               'password': PASSWORD,
               'host': HOST,
               'database': None}

# ---------- PRODUCTS : Search criteria for API ---------- #
HEADERS = {"User-Agent": "P5_substitute - GNU/Linux - Version 0.1"}
PAYLOAD = {"search_simple": 1,
           "action": "process",
           "tagtype_0": "countries",
           "tag_contains_0": "contains",
           "tag_0": "france",
           "sort_by": "unique_scans_n",
           "page_size": 1500,
           "json": 1,
           "fields": "brands,url,stores,nutriscore_grade,"
                     "categories,product_name_fr,code"
           # field make the request faster
           }
