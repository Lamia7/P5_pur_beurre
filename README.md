# P5_pur_beurre
[Trello](https://trello.com/b/SQKs95Pk/projet-5-utilisez-les-donn%C3%A9es-publiques-de-lopenfoodfacts) <br/>
Program only available in French for now.

## Context
The startup Pur Beurre is very familiar with French food habits. Their restaurant, Ratatouille, has become increasingly popular and attracts more and more visitors to the Butte de Montmartre.

The team noticed that their users wanted to change their diet but didn’t know what to start with. 

Replace the Nutella with a hazelnut paste, yes, but which one? And in which store to buy it?

Their idea is to create a program that would interact with the Open Food Facts database to retrieve the food, compare it, and provide the user with a healthier alternative to the food they crave.

## Installation and configuration :computer:
**Install Python**  <br/>
Python 3.8 using the official documentation  <br/>
**Install MySQL**  <br/>
MySQL 8 using the official documentation  <br/>
**Configure MySQL**  <br/>
Start MySQL services using the official documentation  <br/>  <br/>
**Create a user with all privileges:**
```sql
CREATE USER 'root'@'localhost' IDENTIFIED BY 'lamia;
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost';
```
If you want to change the USER and PASSWORD, you will have to modify the config.py file.

**Clone the repository from Github by running this command:**  <br/>
```git clone https://github.com/Lamia7/P5_pur_beurre```

**Execute with a virtual environment:**
1)	Create a virtual environment: `virtualenv -p python3 env`
2)	Activate the virtual environment: `source env/bin/activate`
3)	Install all the libraries through the requirements file: `pip install -r requirements.txt`
4)	Run the application: `python P5_pur_beurre/app.py`

(To deactivate the virtual environment: deactivate)

## To use the program :blue_book:
Run the command `python P5_pur_beurre/app.py`  <br/>
Follow the instructions and use the keyboard to enter your choices (letters and numbers).

## Features :clipboard:
*	Select a category with unhealthy products
*	Select a product from the selected category
*	Display the details of the selected product (name, brands, barcode, OpenFoodFacts’ URL, nutriscore, categories, stores)
*	Find substitutes for the selected product (healthier products)
*	Select a substitute to display its details
*	Save the substitute in a favorite list
*	Consult the list of favorite substitutes with details of each
*	Update a database
*	Delete the list of favorite substitutes
*	Go back to main menu
*	Quit the program

## Tools used to create this program :wrench:
IDE [PyCharm](https://www.jetbrains.com/fr-fr/pycharm/)  <br/>
API [OpenFoodFacts](https://fr.openfoodfacts.org/)  <br/>
Python 3.8  <br/>
MySQL 8 <br/>
MySQL Workbench (for the Physical Data Model)

And a lot of research ...

## Author :pencil:
[Lamia7](https://github.com/Lamia7)


#### Cheklist :memo:
- [x] Find the info we will need for the database
- [x] Create the tables
- [x] Create the foreign keys
- [x] Choose which data to get from OFF API
- [x] Create database with empty tables
- [x] Check how to get data by batch/pack to optimize
- [x] Get data from OFF API
- [x] Clean data from API
- [x] Avoid duplicates
- [x] Insert data to tables
- [x] Insert data to association tables
- [x] Create algorithm to find data (categories)
- [x] Create algorithm to find data (products from category with nutriscore > C)
- [x] Create algorithm to find data (products from similar category list with nutriscore_substitute < nutriscore_product)
- [x] Manage inputs
- [x] Add stores details of the chosen substitute
- [x] Create algorithm to save substitute into favorite table
- [x] Add option to consult list of favorites (SQL query+algorithm)
- [x] Add option to update database (delete/recreate)
- [x] Add option to update favorite table (delete/recreate)
- [x] Create a requirements.txt file
- [x] Check PEP8 with flake 8
