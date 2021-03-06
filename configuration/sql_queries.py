"""SQL queries used in other files"""

from configuration.config import DATABASE_NAME

# -------- GENERAL DATABASE CREATION QUERIES -------- #
CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS " \
                + DATABASE_NAME + " DEFAULT CHARACTER SET utf8mb4;"
USE_DATABASE = "USE " + DATABASE_NAME + ";"

# -------- TABLE CREATION QUERIES -------- #

TABLES = {}
TABLES['product'] = ("CREATE TABLE IF NOT EXISTS `product` ("
                     "`id` INT UNSIGNED AUTO_INCREMENT,"
                     "`name` VARCHAR(150) NOT NULL,"
                     "`nutriscore_grade` CHAR(1) NOT NULL,"
                     "`barcode` BIGINT UNSIGNED NOT NULL,"
                     "`brands` VARCHAR(100) NOT NULL,"
                     "`url` VARCHAR(250) NOT NULL,"
                     "PRIMARY KEY (`id`),"
                     "UNIQUE (barcode))"
                     "ENGINE = InnoDB;")

TABLES['category'] = ("CREATE TABLE IF NOT EXISTS `category` ("
                      "`id` INT UNSIGNED AUTO_INCREMENT,"
                      "`name` VARCHAR(100) NOT NULL,"
                      "PRIMARY KEY (`id`),"
                      "UNIQUE (name))"
                      "ENGINE = InnoDB;")

TABLES['store'] = ("CREATE TABLE IF NOT EXISTS `store` ("
                   "`id` INT UNSIGNED AUTO_INCREMENT,"
                   "`name` VARCHAR(200) NOT NULL,"
                   "PRIMARY KEY (`id`),"
                   "UNIQUE (name))"
                   "ENGINE = InnoDB;")

TABLES['favorite'] = ("CREATE TABLE IF NOT EXISTS `favorite` ("
                      "`id` INT UNSIGNED AUTO_INCREMENT,"
                      "`name` VARCHAR(150) NOT NULL,"
                      "`nutriscore_grade` CHAR(1) NOT NULL,"
                      "`barcode` BIGINT UNSIGNED NOT NULL,"
                      "`brands` VARCHAR(100) NOT NULL,"
                      "`url` VARCHAR(250) NOT NULL,"
                      "`store` VARCHAR(200) NOT NULL,"
                      "PRIMARY KEY (`id`))"
                      "ENGINE = InnoDB;")

TABLES['product_category'] = ("CREATE TABLE IF NOT EXISTS `product_category` ("
                              "`product_id` INT UNSIGNED NOT NULL,"
                              "`category_id` INT UNSIGNED NOT NULL,"
                              "FOREIGN KEY (`product_id`)"
                              "REFERENCES "
                              + DATABASE_NAME
                              + ".`product` (`id`)"
                              "ON DELETE CASCADE "
                              "ON UPDATE NO ACTION,"
                              "FOREIGN KEY (`category_id`)"
                              "REFERENCES "
                              + DATABASE_NAME + ".`category` (`id`))"
                              "ENGINE = InnoDB;")

TABLES['product_store'] = ("CREATE TABLE IF NOT EXISTS `product_store` ("
                           "`product_id` INT UNSIGNED NOT NULL,"
                           "`store_id` INT UNSIGNED NOT NULL,"
                           # "PRIMARY KEY (`product_id`, `store_id`),"
                           "FOREIGN KEY (`product_id`)"
                           "REFERENCES "
                           + DATABASE_NAME
                           + ".`product` (`id`)"
                           "ON DELETE CASCADE "
                           "ON UPDATE NO ACTION,"
                           "FOREIGN KEY (`store_id`)"
                           "REFERENCES "
                           + DATABASE_NAME + ".`store` (`id`))"
                           "ENGINE = InnoDB;")


# -------- INSERTION QUERIES -------- #

INSERT_PRODUCTS = ("INSERT IGNORE INTO product"
                   "(name, brands, barcode, url, nutriscore_grade) "
                   "VALUES (%(name)s, %(brands)s, %(barcode)s, %(url)s, "
                   "%(nutriscore_grade)s) "
                   "ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);")

INSERT_CATEGORIES = "INSERT IGNORE INTO category (name) VALUES (%(name)s) " \
                    "ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);"

INSERT_STORES = "INSERT IGNORE INTO store (name) VALUES (%(name)s) " \
                "ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);"
# if duplicate of store, keep same id

INSERT_PRODUCT_CATEGORY = "INSERT INTO product_category " \
                          "(product_id, category_id) " \
                          "VALUES (" \
                          "%(product_id)s, %(category_id)s);"

INSERT_PRODUCT_STORE = "INSERT INTO product_store (product_id, store_id) " \
                       "VALUES (" \
                       "%(product_id)s, %(store_id)s);"

INSERT_FAVORITE = "INSERT INTO favorite " \
                  "(name, nutriscore_grade, barcode, brands, url, store) " \
                  "VALUES (%(name)s, %(nutriscore_grade)s, %(barcode)s, " \
                  "%(brands)s, %(url)s, %(store)s) " \
                  "ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);"

# -------- SELECTION QUERIES -------- #
SELECT_CATEGORY_MIN_10_PRODUCTS = "SELECT category.id, category.name " \
                                  "FROM category " \
                                  "LEFT JOIN product_category " \
                                  "ON " \
                                  "category.id = " \
                                  "product_category.category_id " \
                                  "GROUP BY category.id " \
                                  "HAVING SUM(product_category.product_id) " \
                                  ">= 10 " \
                                  "LIMIT 10;"

SELECT_CATEGORY_WITH_UNHEALTHY_PRODUCTS = "SELECT " \
                                          "category.id, category.name " \
                                          "FROM category " \
                                          "LEFT JOIN product_category " \
                                          "ON " \
                                          "category.id = " \
                                          "product_category.category_id " \
                                          "RIGHT JOIN product " \
                                          "ON " \
                                          "product_category.product_id = " \
                                          "product.id " \
                                          "WHERE nutriscore_grade = 'C' " \
                                          "OR nutriscore_grade = 'D' " \
                                          "OR nutriscore_grade = 'E' " \
                                          "GROUP BY category.id " \
                                          "HAVING SUM" \
                                          "(product_category.product_id) " \
                                          ">= 5 " \
                                          "LIMIT 10;"

SELECT_PRODUCTS_FROM_CATEGORY = "SELECT " \
                                "product.id, product.name, product.brands, " \
                                "product.nutriscore_grade, product.url " \
                                "FROM product " \
                                "LEFT JOIN product_category " \
                                "ON " \
                                "product.id = product_category.product_id " \
                                "RIGHT JOIN category " \
                                "ON " \
                                "category.id = product_category.category_id " \
                                "WHERE category.id = %s " \
                                "AND " \
                                "(product.nutriscore_grade >= 'D') " \
                                "GROUP BY product.id " \
                                "LIMIT 10"

SELECT_SUBSTITUTES_BY_PRODUCT = "SELECT P.id AS product_id, " \
                                "P.name AS product_name, " \
                                "P.nutriscore_grade AS product_nutriscore, " \
                                "COUNT" \
                                "(product_category.product_id) " \
                                "AS similar_categories, " \
                                "S.id AS substitute_id, " \
                                "S.name AS substitute_name, " \
                                "S.nutriscore_grade " \
                                "AS substitute_nutriscore " \
                                "FROM product P " \
                                "INNER JOIN product S " \
                                "LEFT JOIN product_category " \
                                "ON P.id = product_category.product_id " \
                                "RIGHT JOIN category " \
                                "ON " \
                                "category.id = product_category.category_id " \
                                "WHERE P.id = %s " \
                                "AND " \
                                "P.nutriscore_grade > S.nutriscore_grade " \
                                "GROUP BY S.id " \
                                "HAVING similar_categories >= 2 " \
                                "ORDER BY similar_categories DESC " \
                                "LIMIT 10;"

SELECT_SUBSTITUTE = "SELECT * FROM product WHERE id = %s"

SELECT_STORE = "SELECT store.name " \
               "FROM store " \
               "LEFT JOIN product_store " \
               "ON store.id = product_store.store_id " \
               "RIGHT JOIN product ON product_store.product_id = product.id " \
               "WHERE product.id = %s"

SELECT_FAVORITE = "SELECT * FROM favorite;"

# -------- DELETE QUERIES -------- #
DELETE_DATABASE = "SET FOREIGN_KEY_CHECKS=0; DROP DATABASE IF EXISTS " \
                  + DATABASE_NAME + ";"
DELETE_FAVORITE_DATA = "SET FOREIGN_KEY_CHECKS=0; TRUNCATE TABLE favorite;"
