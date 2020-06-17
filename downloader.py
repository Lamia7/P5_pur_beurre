import requests
import time
import config
from models.product import Product


class Downloader:
    """Class that downloads the chosen data from OFF api"""

    def get_popular_products(self):
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
        return products  # list of dictionaries

    def get_products_details(self):
        products = self.get_popular_products()
        my_products = []

        for one_product in products:
            my_product = Product(one_product.get('product_name_fr'),  # default: none
                                 one_product.get('categories'),
                                 one_product.get('brands'),
                                 one_product.get('code'),
                                 one_product.get('stores', "NOT FOUND"),
                                 one_product.get('url'),
                                 one_product.get('nutriscore_grade')
                                 )

            my_products.append(my_product)
        return my_products

    def display_products(self):
        """Displays each product's details
        chaine = str(product)"""
        my_products = self.get_products_details()
        print(len(my_products))  # number of downloaded products
        for one_product in my_products:
            print(str(one_product))


download = Downloader()
download.display_products()
