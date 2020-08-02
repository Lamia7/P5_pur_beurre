"""Module that handles the app menu"""
import mysql.connector as mc
import config as conf
import sql_queries
from favorite import Favorite, FavoriteManager


class Menu:

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.favorite = None
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
            self.display_favorite()
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

            print(f" ------------------------------------------------------------------ \n "
                  f"                      LISTE DE CATEGORIES: \n "
                  f"------------------------------------------------------------------- \n")
            for category in result:
                print(
                    f"IDENTIFIANT: {category[0]} || CATEGORIE: {category[1]}")  # shows each tuple from the tuples list

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

        rep = input(f"\n-------------------------------------ETAPE 1-------------------------------------- \n "
                    f"Veuillez sélectionner une catégorie parmi la liste ci-dessus avec l'identifiant. \n "
                    f"---------------------------------------------------------------------------------- \n"
                    f"----------------------AUTRES OPTIONS---------------------- \n"
                    f"(M] Retour au menu principal || [Q] Quitter le programme. |\n"
                    f"-----------------------------------------------------------\n"
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
            self.listen_choice_two(id_category_list)

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

            print(f"  -----------------------------------------------------------------------  \n "
                  f"                           LISTE DE PRODUITS \n "
                  f"------------------------------------------------------------------------- \n")
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

        rep = input(f"-----------------------AUTRES OPTIONS----------------------- \n"
                    f"(M] Retour au menu principal || [Q] Quitter le programme.   |\n"
                    f"------------------------------------------------------------\n"
                    f"-------------------------------------ETAPE 2---------------------------------------  \n "
                    f"Choisissez un produit parmi la liste ci-dessus avec l'identifiant. \n "
                    f"----------------------------------------------------------------------------------- \n"
                    f">> [Entrez un identifiant] : ")

        if rep in id_product_list:
            self.find_substitute(rep)
        elif rep.upper() == "M":
            self.display_menu()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                  "...")
            self.listen_choice_three(id_product_list)

    def find_substitute(self, input_product_id):
        """
        Method that finds substitutes of selected product
        + displays them
        + generates list of substitutes' ids
        + displays substitutes' details with stores
        + asks question 3
        """
        self.connect()
        id_substitute_list = []

        # Displays list of substitutes of the chosen product
        try:
            self.cursor.execute(sql_queries.USE_DATABASE)
            self.cursor.execute(sql_queries.SELECT_SUBSTITUTES_BY_PRODUCT, (input_product_id,))
            result = self.cursor.fetchall()

            print(f" ----------------------------------------------------------------------------------- \n "
                  f"Veuillez sélectionner un substitut parmi la liste suivante pour afficher plus de détails : \n "
                  f"------------------------------------------------------------------------------------------------ \n")

            # Prints each substitute from list
            for substitute in result:
                print(f"________________________\n"
                      f"IDENTIFIANT: {substitute[4]}\n"
                      f"NOM SUBSTITUT: {substitute[5]}\n"
                      f"NUTRISCORE: {substitute[6]}\n")

            # Handles chosen substitute
            rep = input(f"-----------------------AUTRES OPTIONS----------------------- \n"
                        f"(M] Retour au menu principal || [Q] Quitter le programme.   |\n"
                        f"------------------------------------------------------------\n"
                        f"-------------------------------------ETAPE 3---------------------------------------  \n "
                        f"Choisissez un substitut parmi la liste ci-dessus pour afficher plus de détails \n "
                        f"----------------------------------------------------------------------------------- \n"
                        f">> [Entrez un identifiant] : ")

            # Adds each substitute's id to a list
            for substitute in result:
                id_substitute_list.append(str(substitute[4]))

            # Checks if substitute's id in input is valid
            if rep in id_substitute_list:
                self.display_substitute(rep)
            elif rep.upper() == "M":
                self.display_menu()
            elif rep.upper() == "Q":
                self.quit_program()
            # If substitute's id in input is invalid
            else:
                print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                      "...")
                self.find_substitute(input_product_id)

        except mc.Error as err:
            print(f"Unsuccessful selection of substitute: {err}")

        # self.display_question_four(favorite)

    def display_substitute(self, rep):
        """Method that displays the chosen substitute"""
        self.connect()

        try:
            self.cursor.execute(sql_queries.USE_DATABASE)
            self.cursor.execute(sql_queries.SELECT_SUBSTITUTE, (rep,))
            chosen_substitute = self.cursor.fetchone()

            # Finds substitute's store(s)
            self.cursor.execute(sql_queries.SELECT_STORE, (rep,))
            stores_substitute_list = self.cursor.fetchall()
            store_substitute = [''.join(store) for store in stores_substitute_list]

            print(f"______________________________________________________________\n"
                  f"Voici les détails du substitut choisi :\n\n"
                  f"IDENTIFIANT........: {chosen_substitute[0]}\n"
                  f"NOM................: {chosen_substitute[1]}\n"
                  f"MARQUE.............: {chosen_substitute[4]}\n"
                  f"CODE BARRE.........: {chosen_substitute[3]}\n"
                  f"NUTRISCORE.........: {chosen_substitute[2]}\n"
                  f"URL Openfoodfacts..: {chosen_substitute[5]}\n"
                  f"LIEU(X) DE VENTE...: {store_substitute}\n"
                  f"______________________________________________________________\n")

            # Creates a favorite object
            self.favorite = Favorite(chosen_substitute[1],
                                     chosen_substitute[2],
                                     chosen_substitute[3],
                                     chosen_substitute[4],
                                     chosen_substitute[5],
                                     str(store_substitute))

            self.disconnect()

        except mc.Error as err:
            print(f"Unsuccessful selection of substitute details with stores: {err}")

        self.display_question_four(self.favorite)

    def display_question_four(self, favorite):
        rep = input(f"\n----------------QUESTION 4-------------------\n"
                    f"Que souhaitez-vous faire ?\n\n"
                    f"[S] - Sauvegarder le substitut.\n"
                    f"(M] - Retour au menu principal.\n"
                    f"[Q] - Quitter le programme.\n"
                    f"-----------------------------------------------\n"
                    f">> [Entrez votre choix] : ")

        if rep.upper() == "S":
            fm = FavoriteManager()
            fm.insert_favorite(favorite)
            print(f"Votre substitut a été sauvegardé dans vos favoris.")
        elif rep.upper() == "M":
            self.display_menu()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                  "...")
            self.display_question_four(favorite)

    def display_favorite(self):
        """
        Method that displays all the favorite substitutes from favorite table
        """
        self.connect()
        try:
            self.cursor.execute(sql_queries.USE_DATABASE)
            self.cursor.execute(sql_queries.SELECT_FAVORITE)
            favorite_list = self.cursor.fetchall()

            print(f"  -----------------------------------------------------------------------  \n "
                  f"                   LISTE DE SUBSTITUTS ENREGISTRES\n "
                  f"------------------------------------------------------------------------- \n")

            for favorite in favorite_list:
                print(f"________________________\n"
                      f"IDENTIFIANT: {favorite[0]}\n"
                      f"NOM PRODUIT: {favorite[1]}\n"
                      f"NUTRISCORE: {favorite[2]}\n"
                      f"CODE BARRE: {favorite[3]}\n"
                      f"MARQUE: {favorite[4]}"
                      f"URL: {favorite[5]}\n")

            self.disconnect()
        except mc.Error as err:
            print(f"Unsuccessful selection of favorite table: {err}")

    def quit_program(self):
        """ quitter le program quand appelée"""
        print(f"------------------------------------------------- \n"
              "OK, on arrête tout. C'est l'heure de la sieste.\n"
              "A bientôt ! \n"
              "zzZZZzz....................")


menu = Menu()
