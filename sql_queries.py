"""SQL queries used in other files"""

from config import DATABASE_NAME

# -------- GENERAL DATABASE CREATION QUERIES -------- #
CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS " + DATABASE_NAME + " DEFAULT CHARACTER SET utf8mb4;"
USE_DATABASE = "USE " + DATABASE_NAME + ";"

SHOW_TABLES = "SHOW TABLES;"


# -------- TABLE CREATION QUERIES -------- #

TABLES = {}
TABLES['product'] = ("CREATE TABLE IF NOT EXISTS `product` ("
                     "`id` INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,"
                     "`name` VARCHAR(150) NOT NULL,"
                     "`nutriscore_grade` CHAR(1) NOT NULL,"
                     "`barcode` BIGINT UNSIGNED NOT NULL UNIQUE,"
                     "`brands` VARCHAR(100) NULL,"
                     "`url` TEXT NOT NULL,"
                     "PRIMARY KEY (`id`))"
                     "ENGINE = InnoDB;")

TABLES['category'] = ("CREATE TABLE IF NOT EXISTS `category` ("
                      "`id` INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,"
                      "`name` VARCHAR(255) NOT NULL,"
                      "PRIMARY KEY (`id`))"
                      "DEFAULT CHARACTER SET = utf8mb4;")

TABLES['store'] = ("CREATE TABLE IF NOT EXISTS `store` ("
                   "`id` INT UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,"
                   "`name` VARCHAR(200) NOT NULL UNIQUE,"
                   "PRIMARY KEY (`id`))"
                   "ENGINE = InnoDB;")

TABLES['favorite'] = ("CREATE TABLE IF NOT EXISTS `favorite` ("
                      "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
                      "`name` VARCHAR(150) NULL,"
                      "`nutriscore_grade` CHAR(1) NULL,"
                      "`barcode` BIGINT UNSIGNED NULL,"
                      "`url` TEXT NULL,"
                      "PRIMARY KEY (`id`))"
                      "ENGINE = InnoDB;")

TABLES['product_category'] = ("CREATE TABLE IF NOT EXISTS `product_category` ("
                              "`category_id` INT UNSIGNED NOT NULL,"
                              "`product_id` INT UNSIGNED NOT NULL,"
                              "PRIMARY KEY (`category_id`, `product_id`),"
                              "FOREIGN KEY (`product_id`)"
                              "REFERENCES " + DATABASE_NAME + ".`product` (`id`)"
                                                              "ON DELETE NO ACTION "
                                                              "ON UPDATE NO ACTION,"
                                                              "FOREIGN KEY (`category_id`)"
                                                              "REFERENCES " + DATABASE_NAME + ".`category` (`id`)"
                                                                                              "ON DELETE NO ACTION "  # empeche suppression du parent et enfant (autre option: CASCADE)
                                                                                              "ON UPDATE NO ACTION)"
                                                                                              "ENGINE = InnoDB;")

TABLES['product_store'] = ("CREATE TABLE IF NOT EXISTS `product_store` ("
                           "`product_id` INT UNSIGNED NOT NULL,"
                           "`store_id` INT UNSIGNED NOT NULL,"
                           "PRIMARY KEY (`product_id`, `store_id`),"
                           "FOREIGN KEY (`product_id`)"
                           "REFERENCES " + DATABASE_NAME + ".`product` (`id`)"
                                                           "ON DELETE NO ACTION "
                                                           "ON UPDATE NO ACTION,"
                                                           "FOREIGN KEY (`store_id`)"
                                                           "REFERENCES " + DATABASE_NAME + ".`store` (`id`)"
                                                                                           "ON DELETE NO ACTION "
                                                                                           "ON UPDATE NO ACTION)"
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
                   "(name, brands, barcode, url, nutriscore_grade) ""VALUES (%s, %s, %s, %s, %s)")

INSERT_CATEGORIES = "INSERT IGNORE INTO category (name) VALUES (%s)"

INSERT_STORES = "INSERT IGNORE INTO store (name) VALUES (%s)"
"""---------------
INSERT
INSERT
"""

# -------- SELECTION QUERIES -------- #
"""---------------
SELECT_PRODUCT
SELECT_CATEGORY
SELECT_STORE
SELECT
SELECT
"""
