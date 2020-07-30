"""SQL queries used in other files"""

from config import DATABASE_NAME

# -------- GENERAL DATABASE CREATION QUERIES -------- #
CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS " + DATABASE_NAME + " DEFAULT CHARACTER SET utf8mb4;"
USE_DATABASE = "USE " + DATABASE_NAME + ";"

SHOW_TABLES = "SHOW TABLES;"


# -------- TABLE CREATION QUERIES -------- #

TABLES = {}
TABLES['product'] = ("CREATE TABLE IF NOT EXISTS `product` ("
                     "`id` INT UNSIGNED AUTO_INCREMENT,"
                     "`name` VARCHAR(150) NOT NULL,"
                     "`nutriscore_grade` CHAR(1) NOT NULL,"
                     "`barcode` BIGINT UNSIGNED NOT NULL,"
                     "`brands` VARCHAR(100) NULL,"
                     "`url` VARCHAR(250) NOT NULL,"
                     "PRIMARY KEY (`id`),"
                     "UNIQUE (barcode));")

TABLES['category'] = ("CREATE TABLE IF NOT EXISTS `category` ("
                      "`id` INT UNSIGNED AUTO_INCREMENT,"
                      "`name` VARCHAR(100) NOT NULL,"
                      "PRIMARY KEY (`id`),"
                      "UNIQUE (name));")

TABLES['store'] = ("CREATE TABLE IF NOT EXISTS `store` ("
                   "`id` INT UNSIGNED AUTO_INCREMENT,"
                   "`name` VARCHAR(255) NOT NULL,"
                   "PRIMARY KEY (`id`),"
                   "UNIQUE (name));")

TABLES['favorite'] = ("CREATE TABLE IF NOT EXISTS `favorite` ("
                      "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                      "`name` VARCHAR(150) NULL,"
                      "`nutriscore_grade` CHAR(1) NULL,"
                      "`barcode` BIGINT UNSIGNED NULL,"
                      "`url` TEXT NULL,"
                      "PRIMARY KEY (`id`))"
                      "ENGINE = InnoDB;")

TABLES['product_category'] = ("CREATE TABLE IF NOT EXISTS `product_category` ("
                              "`product_id` INT UNSIGNED NOT NULL,"
                              "`category_id` INT UNSIGNED NOT NULL,"
                              "FOREIGN KEY (`product_id`)"
                              "REFERENCES " + DATABASE_NAME + ".`product` (`id`)"
                                                              "ON DELETE NO ACTION "  
                                                              "ON UPDATE NO ACTION,"
                                                              "FOREIGN KEY (`category_id`)"
                                                              "REFERENCES " + DATABASE_NAME + ".`category` (`id`));")

TABLES['product_store'] = ("CREATE TABLE IF NOT EXISTS `product_store` ("
                           "`product_id` INT UNSIGNED NOT NULL,"
                           "`store_id` INT UNSIGNED NOT NULL,"
                           # "PRIMARY KEY (`product_id`, `store_id`),"
                           "FOREIGN KEY (`product_id`)"
                           "REFERENCES " + DATABASE_NAME + ".`product` (`id`)"
                                                           "ON DELETE NO ACTION "  # empeche suppression du parent et enfant (autre option: CASCADE)
                                                           "ON UPDATE NO ACTION,"
                                                           "FOREIGN KEY (`store_id`)"
                                                           "REFERENCES " + DATABASE_NAME + ".`store` (`id`))"
                                                                                           "ENGINE = InnoDB;")

TABLES['product_substitute'] = ("CREATE TABLE IF NOT EXISTS `food_substitute`.`product_favorite` ("
                                "`product_id` INT UNSIGNED NOT NULL,"
                                "`favorite_id` INT UNSIGNED NOT NULL,"
                                "PRIMARY KEY (`product_id`, `favorite_id`),"
                                "FOREIGN KEY (`product_id`)"
                                "REFERENCES " + DATABASE_NAME + ".`product` (`id`)"
                                                                "ON DELETE NO ACTION "
                                                                "ON UPDATE NO ACTION,"
                                                                "FOREIGN KEY (`favorite_id`)"
                                                                "REFERENCES " + DATABASE_NAME + ".`favorite` (`id`)"
                                                                                                "ON DELETE NO ACTION "
                                                                                                "ON UPDATE NO ACTION)"
                                                                                                "ENGINE = InnoDB;")

# -------- INSERTION QUERIES -------- #

INSERT_PRODUCTS = ("INSERT IGNORE INTO product"
                   "(name, brands, barcode, url, nutriscore_grade) VALUES (%(name)s, %(brands)s, %(barcode)s, %(url)s, %(nutriscore_grade)s) "
                   "ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);")

INSERT_CATEGORIES = "INSERT IGNORE INTO category (name) VALUES (%(name)s) " \
                    "ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);"

INSERT_STORES = "INSERT IGNORE INTO store (name) VALUES (%(name)s) " \
                "ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id);"  # si doublon de store, garder le même id

INSERT_PRODUCT_CATEGORY = "INSERT INTO product_category (product_id, category_id) " \
                          "VALUES (" \
                          "%(product_id)s, %(category_id)s);"

INSERT_PRODUCT_STORE = "INSERT INTO product_store (product_id, store_id) " \
                          "VALUES (" \
                          "%(product_id)s, %(store_id)s);"

# -------- SELECTION QUERIES -------- #
SELECT_CATEGORY_MIN_10_PRODUCTS = "SELECT category.id, category.name FROM category " \
                                  "LEFT JOIN product_category ON category.id = product_category.category_id " \
                                  "GROUP BY category.id HAVING SUM(product_category.product_id) >= 10 " \
                                  "LIMIT 10;"

SELECT_CATEGORY_WITH_UNHEALTHY_PRODUCTS = "SELECT category.id, category.name FROM category " \
                                  "LEFT JOIN product_category ON category.id = product_category.category_id " \
                                  "RIGHT JOIN product ON product_category.product_id = product.id " \
                                  "WHERE nutriscore_grade = 'C' OR nutriscore_grade = 'D' OR nutriscore_grade = 'E' " \
                                  "GROUP BY category.id HAVING SUM(product_category.product_id) >= 5 " \
                                  "LIMIT 10;"

SELECT_PRODUCTS_FROM_CATEGORY = "SELECT product.id, product.name, product.brands, product.nutriscore_grade, product.url FROM product " \
                                "LEFT JOIN product_category ON product.id = product_category.product_id " \
                                "RIGHT JOIN category ON category.id = product_category.category_id " \
                                "WHERE category.id = %s " \
                                "AND (product.nutriscore_grade >= 'D') " \
                                "GROUP BY product.id " \
                                "LIMIT 10"

SELECT_SUBSTITUTES_BY_PRODUCT = "SELECT P.id AS product_id, P.name AS product_name, P.nutriscore_grade AS product_nutriscore, COUNT(product_category.product_id) AS similar_categories, " \
                                "S.id AS substitute_id, S.name AS substitute_name, S.nutriscore_grade AS substitute_nutriscore " \
                                "FROM product P INNER JOIN product S " \
                                "LEFT JOIN product_category " \
                                "ON P.id = product_category.product_id " \
                                "RIGHT JOIN category " \
                                "ON category.id = product_category.category_id " \
                                "WHERE P.id = %s " \
                                "AND P.nutriscore_grade > S.nutriscore_grade " \
                                "GROUP BY S.id " \
                                "HAVING similar_categories >= 2 " \
                                "ORDER BY similar_categories DESC " \
                                "LIMIT 10;"

SELECT_SUBSTITUTE = "SELECT * FROM product WHERE id = %s"

SELECT_STORE = "SELECT store.name " \
               "FROM store " \
               "LEFT JOIN product_store ON store.id = product_store.store_id " \
               "RIGHT JOIN product ON product_store.product_id = product.id " \
               "WHERE product.id = %s"

"""---------------
SELECT_CATEGORY_MIN_10_PRODUCTS = "SELECT category.id, category.name FROM category " \
                                  "LEFT JOIN product_category ON category.id = product_category.category_id " \
                                  "GROUP BY category.id HAVING SUM(product_category.product_id) >= 10 " \
                                  "LIMIT 10;"
 
SELECT_CATEGORY_MIN_10_UNHEALTHY_PRODUCTS = "SELECT category.id, category.name FROM category " \
                                  "LEFT JOIN product_category ON category.id = product_category.category_id " \
                                  "RIGHT JOIN product ON product_category.product_id = product.id " \
                                  "WHERE nutriscore_grade = 'C' OR nutriscore_grade = 'D' OR nutriscore_grade = 'E' " \
                                  "GROUP BY category.id HAVING SUM(product_category.product_id) >= 5 " \
                                  "LIMIT 10;"
---------------------------------------------------
TERMINAL

stores
SELECT store.name 
FROM store 
LEFT JOIN product_store ON store.id = product_store.store_id 
RIGHT JOIN product ON product_store.product_id = product.id 
WHERE product.id = %s

nom des categories unhealthy
SELECT category.id, category.name FROM category 
LEFT JOIN product_category ON category.id = product_category.category_id 
RIGHT JOIN product ON product_category.product_id = product.id 
WHERE nutriscore_grade = 'C' OR nutriscore_grade = 'D' OR nutriscore_grade = 'E' 
GROUP BY category.id HAVING SUM(product_category.product_id) >= 5 
LIMIT 10;

produits unhealthy
SELECT product.id, product.name, product.brands, product.nutriscore_grade, product.url FROM product
LEFT JOIN product_category ON product.id = product_category.product_id
RIGHT JOIN category ON category.id = product_category.category_id
WHERE nutriscore_grade = 'C' OR nutriscore_grade = 'D' OR nutriscore_grade = 'E'
GROUP BY product.id

produits d'une categorie unhealthy
SELECT product.id, product.name, product.brands, product.nutriscore_grade, product.url FROM product
LEFT JOIN product_category ON product.id = product_category.product_id
RIGHT JOIN category ON category.id = product_category.category_id
WHERE category.id = %s
AND (product.nutriscore_grade = 'C' OR product.nutriscore_grade = 'D' OR product.nutriscore_grade = 'E')
GROUP BY product.id

produits similaires plus healthy
SELECT P.id AS prod_id, P.name AS prod_name, P.nutriscore_grade AS prod_nutriscore, 
S.id AS sub_id, S.name AS sub_name, S.nutriscore_grade AS sub_nutriscore   
FROM product P INNER JOIN product S 
LEFT JOIN product_category 
ON P.id = product_category.product_id 
RIGHT JOIN category 
ON category.id = product_category.category_id 
WHERE category.id = 7 

substitut
SELECT P.id AS product_id, P.name AS product_name, P.nutriscore_grade AS product_nutriscore, 
COUNT(product_category.product_id) AS similar_categories, 
S.id AS substitute_id, S.name AS substitute_name, S.nutriscore_grade AS substitute_nutriscore 
FROM product P INNER JOIN product S 
LEFT JOIN product_category 
ON P.id = product_category.product_id 
RIGHT JOIN category 
ON category.id = product_category.category_id 
WHERE P.id = 4 
AND P.nutriscore_grade > S.nutriscore_grade 
GROUP BY S.id 
HAVING similar_categories >= 2 
ORDER BY similar_categories DESC 
LIMIT 10;

(SELECT product_category.product_id 
FROM product_category 
WHERE product_category.category_id = product_category.category_id)
AND 

TEST4


SELECT_STORE
SELECT
SELECT
"""
