import requests
import time
import config
from models.product import Product


class Downloader:
    """Class that downloads the chosen data from OFF api"""

    products = []

    def __init__(self):
        """Gets the thousand most popular products from OFF API"""

        # Manage time between requests
        r = ''
        while r == '':
            # Pause before new request
            time.sleep(1)
            try:
                r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?", params=config.PAYLOAD,
                                 headers=config.HEADERS)
                break
            except:
                print("Connection refused ... Please wait for 5 seconds...")
                print("zzZZzz...")
                time.sleep(5)
                print("Ok, I am back, now let's continue.")
                continue

        # optional
        print(r.url)

        # Assign the products found in a json format into a variable (dictionary)
        products_json = r.json()
        products = products_json["products"]
        self.products = products  # list of dictionaries

    def avoid_empty(self):
        """Gets only products without empty values."""

        products = self.products
        full_products = []
        for p in products:
            if p.get('product_name_fr') \
                    and p.get('categories')\
                    and p.get('brands') \
                    and p.get('code') \
                    and p.get('stores') \
                    and p.get('url') \
                    and p.get('nutriscore_grade') is not None:

                full_products.append(p)
        self.products = full_products
        #print(len(full_products))

    def clean(self):
        """Normalize product's name, categories and stores"""

        clean_products = []
        products = self.products
        for product in products:
            product['product_name_fr'] = set([name.strip().lower().capitalize() for name in product['product_name_fr'].split(',')])
            product['categories'] = set([name.strip().lower().capitalize() for name in product['categories'].split(',')])
            product['stores'] = set([store.strip().upper() for store in product['stores'].split(',')])
            clean_products.append(product)

        return clean_products

    def get_products(self):
        """Gets product objects"""

        clean_products = self.clean()
        products = []
        for one_product in clean_products:
            my_product = Product(one_product['product_name_fr'],
                                 one_product['categories'],
                                 one_product['brands'],
                                 one_product['code'],
                                 one_product['stores'],
                                 one_product['url'],
                                 one_product['nutriscore_grade']
                                 )

            products.append(my_product)
        return products

    def display_products(self):
        """Displays each product's details
        chaine = str(product)"""
        products = self.get_products()
        print(len(products))  # number of downloaded products
        for one_product in products:
            print(str(one_product))
