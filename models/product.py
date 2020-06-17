class Product:
    """Class that creates products"""

    def __init__(self,
                 name,
                 category,
                 brand,
                 barcode,
                 stores,
                 url,
                 nutriscore_grade
                 ):
        """description d'un produit: il a un nom, des catégories, marque, magasins, code, ingrédients, url, nutriscore"""
        self.name = name
        self.category = category
        self.brand = brand
        self.barcode = barcode
        self.stores = stores
        self.url = url
        self.nutriscore_grade = nutriscore_grade

    def __str__(self):
        """String representation of Product object"""
        return f"----------------" \
               f"NAME: {self.name}, | BRAND: {self.brand}, | BARCODE: {self.barcode}" \
               f"| CATEGORY: {self.category}" \
               f"| STORES: {self.stores}" \
               f"| URL: {self.url}" \
               f"| NUTRISCORE: {self.nutriscore_grade}"
