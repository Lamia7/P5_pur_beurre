import time

import requests

from configuration import config
from models.product import Product


class Downloader:
    """Class that downloads the chosen data from OFF api"""

    def __init__(self):
        """Gets the thousand most popular products from OFF API"""

        self.one_product = None
        self.clean_products = []
        self.final_products = []

        # Manage time between requests
        r = ''
        while r == '':
            # Pause before new request
            time.sleep(1)
            try:
                r = requests.get("https://fr.openfoodfacts.org/cgi/search.pl?",
                                 params=config.PAYLOAD,
                                 headers=config.HEADERS)
                break
            except ValueError:
                print("Connexion refusée ... "
                      "Merci de patienter quelques instants...")
                print("zzZZzz...")
                time.sleep(5)  # 5secounds
                print("Ok, c'est repartie, continuons.")
                continue

        # Assign products found in a json format into a variable (dict)
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

    def clean(self):
        """Normalize product's name, categories and stores"""

        # clean_products = []
        products = self.products
        for product in products:
            product['product_name_fr'] = \
                product['product_name_fr'].strip().lower().capitalize()  # str
            product['categories'] = \
                [name.strip().lower().capitalize()
                 for name in product['categories'].split(',')]  # list
            product['stores'] = \
                [store.strip().upper()
                 for store in product['stores'].split(',')]  # list
            product['nutriscore_grade'] = \
                product['nutriscore_grade'].strip().upper()
            # list of dict (products) that contain dictionaries (attributes)
            self.clean_products.append(product)

        return self.clean_products

    def get_products(self):
        """Gets product objects"""

        clean_products = self.clean()
        for one_product_dict in clean_products:
            my_product = Product(one_product_dict)

            self.final_products.append(my_product)
        return self.final_products
