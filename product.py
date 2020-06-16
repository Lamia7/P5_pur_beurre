class Product:
    """Class that creates products"""

    def __init__(self, name, category, brand, barcode, stores, url, nutriscore_grade):
        """description d'un produit: il a un nom, des catégories, marque, magasins, code, ingrédients, url, nutriscore"""
        self.name = name
        self.category = category
        self.brand = brand
        self.barcode = barcode
        self.stores = stores
        self.url = url
        self.nutriscore_grade = nutriscore_grade

    def print_content(self):
        print('-------------------------------')
        print('NAME: ', self.name)
        print('CATEGORY: ', self.category)
        print('BRAND: ', self.brand)
        print('BARCODE: ', self.barcode)
        print('STORES: ', self.stores)
        print('URL: ', self.url)
        print('NUTRISCORE GRADE: ', self.nutriscore_grade)
        print('-------------------------------')