"""Module that handles the app menu"""
import mysql.connector as mc
import config as conf
import sql_queries


class Menu:

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.connect()
        self.display_menu()

    def connect(self):
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def display_menu(self):
        """ Displays main menu and handles inputs """

        b = "OK retrouvons les substituts enregistrés dans la table substitute..."

        print(f" ------------------------------------------ \n"
              f"MENU PRINCIPAL : Que souhaitez-vous faire ?\n "
              f"------------------------------------------ \n")

        rep = input(f"[R] - Rechercher un substitut à un aliment. \n"
                    f"[C] - Consulter mes aliments substitués enregistrés. \n"
                    f"[Q] - Quitter le programme.\n")

        if rep.upper() == "R":  # sets the input in uppercase to listen to lower and upper answer
            self.find_display_categories()
        elif rep.upper() == "C":
            print(b)
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                  "...")
            self.display_menu()

    def find_display_categories(self):
        """
        Method that finds 10 categories from category table with unhealthy products
        + display them
        + generates list of categories' ids
        + calls next question
        """
        cnx = self.cnx
        cursor = self.cursor
        self.connect()

        id_category_list = []

        try:
            cursor.execute(sql_queries.USE_DATABASE)
            cursor.execute(sql_queries.SELECT_CATEGORY_WITH_UNHEALTHY_PRODUCTS)
            result = cursor.fetchall()  # returns tuples list

            print(f" ------------------------------------------------------------- \n "
                  f"Veuillez sélectionner une catégorie parmi la liste suivante : \n "
                  f"------------------------------------------------------------- \n")
            for category in result:
                print(f"\n {category}")  # shows each tuple from the tuples list

            # List of categories' ids used to verify input
            for i, category in result:
                id_category_list.append(str(i))  # convert id as string to be used later to compare with input

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful selection of categories with unhealthy products: {err}")

        self.display_question_two(id_category_list)

    def display_question_two(self, id_category_list):
        """
        Method that ask 2nd question (choose a category from list)
        + listen to answers (which category's id)
        + offers other options (quit or back to main menu)
        """

        rep = input(f"\n------------------------- \n"
                    f"(M] - Retour au menu principal.\n"
                    f"[Q] - Quitter le programme.\n")

        if rep in id_category_list:
            print(type(rep))
            self.find_display_products_by_category(rep)
        elif rep.upper() == "M":
            self.display_menu()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                  "...")
            self.display_menu()

    def find_display_products_by_category(self, input_cat_id):
        """
        Method that finds unhealthy products from selected category
        + displays them
        + print() et input() between:
        si input(entre 1 et 5) : find_substitute()
        si input("2") quit_program()

        """
        cnx = self.cnx
        cursor = self.cursor
        self.connect()

        #id_product_list = []

        try:
            cursor.execute(sql_queries.USE_DATABASE)
            cursor.execute(sql_queries.SELECT_PRODUCTS_FROM_CATEGORY, (input_cat_id,))
            result = cursor.fetchall()  # returns tuples list

            print(f" ------------------------------------------------------------- \n "
                  f"Veuillez sélectionner un produit parmi la liste suivante : \n "
                  f"------------------------------------------------------------- \n")
            for product in result:
                print(f"\n {product}")  # shows each tuple from the tuples list

            # List of product' ids used to verify input
            #for product[0] in result:
                #id_product_list.append(str(product[0]))  # convert id as string to be used later to compare with input

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful selection of categories with unhealthy products: {err}")

       # print(id_product_list)
        #self.display_question_three(id_product_list)

    def display_question_three(self):
    #def display_question_three(self, id_product_list):

        rep = input(f"\n------------------------- \n"
                    f"(M] - Retour au menu principal.\n"
                    f"[Q] - Quitter le programme.\n")

        #if rep in id_product_list:
            #print(type(rep))
            #self.find_substitute(rep)
        if rep.upper() == "M":
            self.display_menu()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                  "...")
            self.display_menu()

    def find_substitute(self, id_product_list):
        """
        find product(s) where nutriscore < selected_product_nutriscore
        + afficher/display
        + print() et input() between:
        1 - Enregistrer le résultat dans la base de données.
        2 - Quitter le programme.

        si input(1) : save_substitute()
        si input("2") quit_program()
        """
        pass

    def save_substitute(self):
        pass

    def quit_program(self):
        """ quitter le program quand appelée"""
        print(f"------------------------------------------------- \n"
              "OK, on arrête tout. C'est l'heure de la sieste.\n"
              "A bientôt ! \n"
              "zzZZZzz....................")


menu = Menu()
