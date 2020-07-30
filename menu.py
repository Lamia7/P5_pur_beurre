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
        """Method that connects MySQL server"""
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def disconnect(self):
        """Method that disconnects MySQL server"""
        self.cursor.close()
        self.cnx.close()

    def execute(self, query):

        """
        def execute(self, query, flag=False):
        :param query:
        :param flag:
        :return:

        flags = {
            isSelect: True
        }
        if flag:
            return self.cursor.fetchall()

        et pr appeler self.execute(sql_queries.SELECT_CATEGORY_WITH_UNHEALTHY_PRODUCTS)
        """

        self.cursor.execute(sql_queries.USE_DATABASE)
        self.cursor.execute(query)

        return self.cursor.fetchall()

    def display_menu(self):
        """ Displays main menu and handles inputs """

        b = "OK retrouvons les substituts enregistrés dans la table substitute..."

        print(f" ------------------------------------------ \n"
              f"MENU PRINCIPAL : Que souhaitez-vous faire ?\n "
              f"------------------------------------------ \n")

        rep = input(f"[R] - Rechercher un substitut à un aliment.\n"
                    f"[C] - Consulter mes aliments substitués enregistrés.\n"
                    f"[Q] - Quitter le programme.\n"
                    f">> [Entrez votre choix] : ")

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
        + asks question 1
        """

        self.connect()
        id_category_list = []

        try:
            self.cursor.execute(sql_queries.USE_DATABASE)
            self.cursor.execute(sql_queries.SELECT_CATEGORY_WITH_UNHEALTHY_PRODUCTS)
            result = self.cursor.fetchall()  # returns tuples list

            print(f" -----------------------------------QUESTION 1------------------------------------ \n "
                  f"Veuillez sélectionner une catégorie parmi la liste suivante avec l'identifiant: \n "
                  f"---------------------------------------------------------------------------------- \n")
            for category in result:
                print(f"IDENTIFIANT: {category[0]} || CATEGORIE: {category[1]}")  # shows each tuple from the tuples list

            # List of categories' ids used to verify input
            for i, category in result:
                id_category_list.append(str(i))  # convert id as string to be used later to compare with input

            self.disconnect()
        except mc.Error as err:
            print(f"Unsuccessful selection of categories with unhealthy products: {err}")

        self.listen_choice_two(id_category_list)

    def listen_choice_two(self, id_category_list):
        """
        Method that handles inputs (answers) to 2nd question (which category's id from list)
        + offers other options (quit or back to main menu)
        """

        rep = input(f"\n------------------------OPTIONS------------------------ \n"
                    f"(M] Retour au menu principal || [Q] Quitter le programme.\n"
                    f">> [Entrez un identifiant] : ")

        if rep in id_category_list:  # rep is a str
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
        + generates list of products' ids
        + asks question 2
        """

        self.connect()
        id_product_list = []

        try:
            self.cursor.execute(sql_queries.USE_DATABASE)
            self.cursor.execute(sql_queries.SELECT_PRODUCTS_FROM_CATEGORY, (input_cat_id,))
            result = self.cursor.fetchall()  # returns tuples list

            print(f"  -----------------------------------QUESTION 2------------------------------------  \n "
                  f"Veuillez sélectionner un produit parmi la liste suivante avec l'identifiant: \n "
                  f"----------------------------------------------------------------------------------- \n")
            for product in result:
                print(f"________________________\n"
                      f"IDENTIFIANT: {product[0]}\n"
                      f"NOM PRODUIT: {product[1]}\n"
                      f"MARQUE: {product[2]}\n"
                      f"NUTRISCORE: {product[3]}\n"
                      f"URL: {product[4]}\n")  # shows each index of tuple from the tuples list

            # Adds 1st index (product_id) from list of products
            for product in result:
                id_product_list.append(str(product[0]))

            self.disconnect()
        except mc.Error as err:
            print(f"Unsuccessful selection of unhealthy products: {err}")

        self.listen_choice_three(id_product_list)

    def listen_choice_three(self, id_product_list):
        """
        Method that handles inputs (answers) to 3rd question (which product's id from list)
        + offers other options (quit or back to main menu)
        """

        rep = input(f"\n------------------------OPTIONS------------------------ \n"
                    f"(M] Retour au menu principal || [Q] Quitter le programme.\n"
                    f">> [Entrez un identifiant] : ")

        if rep in id_product_list:
            self.find_substitute(rep)
        if rep.upper() == "M":
            self.display_menu()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                  "...")
            self.display_menu()

    def find_substitute(self, input_product_id):
        """
        Method that finds substitutes of selected product
        + displays them
        + generates list of substitutes' ids
        + asks question 3
        """
        self.connect()
        id_substitute_list = []

        try:
            self.cursor.execute(sql_queries.USE_DATABASE)
            self.cursor.execute(sql_queries.SELECT_SUBSTITUTES_BY_PRODUCT, (input_product_id,))
            result = self.cursor.fetchall()

            print(f" ------------------------------------------QUESTION 3------------------------------------------- \n "
                  f"Veuillez sélectionner un substitut parmi la liste suivante pour afficher plus de détails : \n "
                  f"------------------------------------------------------------------------------------------------ \n")

            # Prints each substitute from list
            for substitute in result:
                print(f"________________________\n"
                      f"IDENTIFIANT: {substitute[4]}\n"
                      f"NOM SUBSTITUT: {substitute[5]}\n"
                      f"NUTRISCORE: {substitute[6]}\n")

            print(f"\n------------------------OPTIONS------------------------ \n"
                  f"(M] Retour au menu principal || [Q] Quitter le programme.\n"
                  f">> [Entrez un identifiant] : ")

            # Handles chosen substitute
            rep = input()
            for substitute in result:
                id_substitute_list.append(str(substitute[4]))  # adds each substitute's id to a list
            if rep in id_substitute_list:  # checks if substitute's id in input is valid
                self.cursor.execute(sql_queries.SELECT_SUBSTITUTE, (rep,))
                chosen_substitute = self.cursor.fetchone()
                print(f"______________________________________________________________\n"
                      f"Voici les détails du substitut choisi :\n\n"
                      f"IDENTIFIANT........: {chosen_substitute[0]}\n"
                      f"NOM................: {chosen_substitute[1]}\n"
                      f"MARQUE.............: {chosen_substitute[4]}\n"
                      f"CODE BARRE.........: {chosen_substitute[3]}\n"
                      f"NUTRISCORE.........: {chosen_substitute[2]}\n"
                      f"URL Openfoodfacts..: {chosen_substitute[5]}\n"
                      f"______________________________________________________________\n")

            self.disconnect()
        except mc.Error as err:
            print(f"Unsuccessful selection of substitute: {err}")

        self.display_question_four()

    def display_question_four(self):
        rep = input(f"\n----------------QUESTION 4-------------------\n"
                    f"Que souhaitez-vous faire ?\n\n"
                    f"[S] - Sauvegarder le substitut.\n"
                    f"(M] - Retour au menu principal.\n"
                    f"[Q] - Quitter le programme.\n"
                    f"-----------------------------------------------")

        if rep.upper() == "S":
            print(f"Sauvegardons ce substitut.")
            #self.save_substitute()
        if rep.upper() == "M":
            self.display_menu()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                  "...")
            self.display_menu()

    def save_substitute(self):
        pass

    def quit_program(self):
        """ quitter le program quand appelée"""
        print(f"------------------------------------------------- \n"
              "OK, on arrête tout. C'est l'heure de la sieste.\n"
              "A bientôt ! \n"
              "zzZZZzz....................")


menu = Menu()
