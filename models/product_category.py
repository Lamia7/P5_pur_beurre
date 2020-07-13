import mysql.connector as mc
import config as conf
import sql_queries


class ProductCategory:

    def __init__(self, product_id, category_id):
        self.product_id = product_id
        self.category_id = category_id

    def __str__(self):
        """String representation of ProductCategory object"""
        return f"product_id: {self.product_id}, category_id: {self.category_id}"


class ProductCategoryManager:
    """Manages category data"""

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def insert_product_and_category_ids(self, product_category_obj_list):
        """From a list of objects ProductCategory (product_category_obj_list),
        this method creates a list of dict that affects id product to 'product_id'
        and id category to 'category_id'
        """

        cnx = self.cnx
        cursor = self.cursor
        self.connect()

        data_product_category_list = []
        for product_category_ob in product_category_obj_list:
            data_product_category_list.append(
                {'product_id': product_category_ob.product_id, 'category_id': product_category_ob.category_id})

        print(f"data_product_category_list : {data_product_category_list}")

        try:
            cursor.execute(sql_queries.USE_DATABASE)
            for prod_cat_dict in data_product_category_list:
                cursor.execute(sql_queries.INSERT_PRODUCT_CATEGORY, prod_cat_dict)
            cnx.commit()

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful insertion of product_id and category_id: {err}")
