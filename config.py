"""Configuration file for optimization of other files"""

# PRODUCTS : Search criteria for API
HEADERS = {"User-Agent": "P5_substitute - GNU/Linux - Version 0.1"}
PAYLOAD = {"search_simple": 1,
           "action": "process",
           "tagtype_0": "countries",
           "tag_contains_0": "contains",
           "tag_0": "france",
           "sort_by": "unique_scans_n",
           "page_size": 1000,
           "json": 1,
           "fields": "brands,url,stores,nutriscore_grade,categories,product_name_fr,code"  # make the request faster
           }