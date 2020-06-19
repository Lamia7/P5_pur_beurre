"""SQL queries used in other files"""

# ---- GENERAL DATABASE CREATION QUERIES ---- #

CREATE_SCHEMA = "CREATE SCHEMA IF NOT EXISTS `food_substitute` DEFAULT CHARACTER SET utf8mb4 ;"
USE_DATABASE = "USE `food_substitute` ;"

SHOW_TABLES = "SHOW TABLES ;"


# ---- CREATION QUERIES ---- #

CREATE_PRODUCT_TABLE = "CREATE TABLE IF NOT EXISTS `food_substitute`.`product` (" \
                       "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                       "`name` VARCHAR(150) COLLATE 'Default Collation' NOT NULL," \
                       "`nutriscore` CHAR(1) NOT NULL," \
                       "`barcode` BIGINT UNSIGNED NOT NULL," \
                       "`brand` VARCHAR(100) NULL," \
                       "`url` TEXT NOT NULL," \
                       "PRIMARY KEY (`id`))" \
                       "ENGINE = InnoDB" \
                       "DEFAULT CHARACTER SET = utf8mb4;"

CREATE_CATEGORY_TABLE = "CREATE TABLE IF NOT EXISTS `food_substitute`.`category` (" \
                        "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                        "`name` VARCHAR(100) NOT NULL," \
                        "PRIMARY KEY (`id`))" \
                        "DEFAULT CHARACTER SET = utf8mb4;"

CREATE_STORE_TABLE = "CREATE TABLE IF NOT EXISTS `food_substitute`.`store` (" \
                     "`id` INT UNSIGNED NOT NULL AUTO_INCREMENT," \
                     "`name` VARCHAR(100) NOT NULL," \
                     "PRIMARY KEY (`id`))" \
                     "ENGINE = InnoDB" \
                     "DEFAULT CHARACTER SET = utf8mb4;"

CREATE_FAVORITE_TABLE = "CREATE TABLE IF NOT EXISTS `food_substitute`.`favorite` (" \
                        "`id` INT UNSIGNED NULL AUTO_INCREMENT," \
                        "`name` VARCHAR(150) NULL," \
                        "`nutriscore` CHAR(1) NULL," \
                        "`barcode` BIGINT UNSIGNED NULL," \
                        "`url` TEXT NULL," \
                        "PRIMARY KEY (`id`))" \
                        "ENGINE = InnoDB" \
                        "DEFAULT CHARACTER SET = utf8mb4;"


# ---- INSERTION QUERIES ---- #
"""---------------
INSERT_PRODUCTS
INSERT_CATEGORIES
INSERT_STORES
INSERT
INSERT
"""

# SELECTION QUERIES
"""---------------
SELECT_PRODUCT
SELECT_CATEGORY
SELECT_STORE
SELECT
SELECT
"""
