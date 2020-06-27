"""SQL queries used in other files"""

from config import DATABASE_NAME

# -------- GENERAL DATABASE CREATION QUERIES -------- #
CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS " + DATABASE_NAME + " DEFAULT CHARACTER SET utf8mb4;"
USE_DATABASE = "USE " + DATABASE_NAME + ";"

SHOW_TABLES = "SHOW TABLES;"


# -------- CREATION QUERIES -------- #

TABLES = {}

TABLES['product'] = "CREATE TABLE IF NOT EXISTS `product` (" \
                       "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                       "`name` VARCHAR(150) NOT NULL," \
                       "`nutriscore_grade` CHAR(1) NOT NULL," \
                       "`barcode` BIGINT UNSIGNED NOT NULL," \
                       "`brands` VARCHAR(100) NULL," \
                       "`url` TEXT NOT NULL," \
                       "PRIMARY KEY (`id`))" \
                       "ENGINE = InnoDB;"

TABLES['category'] = "CREATE TABLE IF NOT EXISTS `category` (" \
                        "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                        "`name` VARCHAR(100) NOT NULL," \
                        "PRIMARY KEY (`id`))" \
                        "DEFAULT CHARACTER SET = utf8mb4;"

TABLES['store'] = "CREATE TABLE IF NOT EXISTS `store` (" \
                     "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                     "`name` VARCHAR(100) NOT NULL," \
                     "PRIMARY KEY (`id`))" \
                     "ENGINE = InnoDB;"

TABLES['favorite'] = "CREATE TABLE IF NOT EXISTS `favorite` (" \
                        "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                        "`name` VARCHAR(150) NULL," \
                        "`nutriscore_grade` CHAR(1) NULL," \
                        "`barcode` BIGINT UNSIGNED NULL," \
                        "`url` TEXT NULL," \
                        "PRIMARY KEY (`id`))" \
                        "ENGINE = InnoDB;"

# -------- INSERTION QUERIES -------- #

INSERT_PRODUCTS = "INSERT IGNORE INTO 'product' (name, brands, barcode, url, nutriscore_grade) " \
                  "VALUES (%s, %s, %s, %s, %s);"

INSERT_CATEGORIES = "INSERT IGNORE INTO 'categories' (name) VALUES (%s);"

INSERT_STORES = "INSERT IGNORE INTO 'stores' (name) VALUES (%s);"
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
