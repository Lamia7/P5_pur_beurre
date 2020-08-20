"""Module that handles the app menus"""
import mysql.connector as mc
from configuration import config as conf, sql_queries as sql
from models.favorite import Favorite, FavoriteManager
from colorama import Fore, Back, Style
from product_management.main import init_database


class Menu:

    def __init__(self):
        self.cnx = None
        self.cursor = None
        self.favorite = None
        self.connect()

    def connect(self):
        """Method that connects MySQL server"""
        self.cnx = mc.connect(**conf.MYSQLCONFIG)
        self.cursor = self.cnx.cursor()  # init cursor
        return self.cursor, self.cnx

    def disconnect(self):
        """Method that disconnects MySQL server"""
        self.cursor.close()
        self.cnx.close()

    def display_menu(self):
        """ Displays main menus and handles inputs """

        print(Back.CYAN, Style.BRIGHT + f" ------------------------------------------ \n"
                                        f"MENU PRINCIPAL : Que souhaitez-vous faire ?\n "
                                        f"------------------------------------------ \n")
        print(Back.RESET, Style.RESET_ALL)
        print(f"[R] - Rechercher un substitut à un aliment.\n"
              f"[C] - Consulter mes substituts enregistrés en favoris.\n"
              f"[S] - Supprimer les substituts enregistrés en favoris.\n"
              f"[X] - Supprimer et réinstaller la base de données.\n"
              f"[Q] - Quitter le programme.\n")
        rep = input(Fore.GREEN + f">> [Entrez votre choix] : ")
        print(Fore.RESET)

        if rep.upper() == "R":  # sets the input in uppercase to listen to lower and upper answer
            self.find_display_categories()
        elif rep.upper() == "C":
            self.display_favorite()
        elif rep.upper() == "S":
            self.delete_favorite()
        elif rep.upper() == "X":
            self.delete_database()
            init_database()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print(Fore.RED + "OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                             "...")
            print(Fore.RESET)
            self.display_menu()

    def delete_favorite(self):
        """Method that deletes favorite substitutes"""
        self.connect()

        try:
            self.cursor.execute(sql.USE_DATABASE)
            self.cursor.execute(sql.DELETE_FAVORITE_DATA)

            print(Fore.CYAN + "Les substituts favoris ont été supprimés avec succès.")
            print(Fore.RESET)

            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de la suppression des substituts enregistrés favoris. Détails de l'erreur: {err}")

    def delete_database(self):
        """Method that deletes database"""

        self.connect()
        try:
            self.cursor.execute(sql.USE_DATABASE)
            self.cursor.execute(sql.DELETE_DATABASE)
            print(Fore.CYAN + "La base de données a été supprimé avec succès.")
            print(Fore.RESET)
            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de la suppression de la base de données. Détails de l'erreur : {err}")

        #init_database()

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
            self.cursor.execute(sql.USE_DATABASE)
            self.cursor.execute(sql.SELECT_CATEGORY_WITH_UNHEALTHY_PRODUCTS)
            result = self.cursor.fetchall()  # returns tuples list

            print(Fore.MAGENTA + f" ------------------------------------------------------------------ \n "
                                 f"                      LISTE DE CATEGORIES: \n "
                                 f"------------------------------------------------------------------- ")
            print(Fore.RESET)
            for category in result:
                print(
                    f"IDENTIFIANT: {category[0]} || CATEGORIE: {category[1]}")  # shows each tuple from the tuples list

            # List of categories' ids used to verify input
            for i, category in result:
                id_category_list.append(str(i))  # convert id as string to be used later to compare with input

            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de la sélection des catégories. Détails de l'erreur : {err}")

        self.listen_choice_two(id_category_list)

    def listen_choice_two(self, id_category_list):
        """
        Method that handles inputs (answers) to 2nd question (which category's id from list)
        + offers other options (quit or back to main menus)
        """
        print(Fore.YELLOW + f"\n----------------------AUTRES OPTIONS---------------------- \n"
                            f"[M] Retour au menus principal || [Q] Quitter le programme. |\n"
                            f"-----------------------------------------------------------\n")

        print(Fore.CYAN + f"-------------------------------------ETAPE 1-------------------------------------- \n "
                          f"Veuillez sélectionner une catégorie parmi la liste ci-dessus avec l'identifiant. \n "
                          f"---------------------------------------------------------------------------------- \n")

        rep = input(Fore.GREEN + f">> [Entrez un identifiant] : ")
        print(Fore.RESET)

        if rep in id_category_list:  # rep is a str
            self.find_display_products_by_category(rep)
        elif rep.upper() == "M":
            self.display_menu()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print(Fore.RED + "OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
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
            self.cursor.execute(sql.USE_DATABASE)
            self.cursor.execute(sql.SELECT_PRODUCTS_FROM_CATEGORY, (input_cat_id,))
            result = self.cursor.fetchall()  # returns tuples list

            print(Fore.MAGENTA + f"  -----------------------------------------------------------------------  \n "
                                 f"                           LISTE DE PRODUITS \n "
                                 f"------------------------------------------------------------------------- ")
            print(Fore.RESET)
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
            print(f"Erreur lors de la sélection de produits malsains. Détails de l'erreur : {err}")

        self.listen_choice_three(id_product_list)

    def listen_choice_three(self, id_product_list):
        """
        Method that handles inputs (answers) to 3rd question (which product's id from list)
        + offers other options (quit or back to main menus)
        """

        print(Fore.YELLOW + f"-----------------------AUTRES OPTIONS----------------------- \n"
                            f"[M] Retour au menus principal || [Q] Quitter le programme.   |\n"
                            f"------------------------------------------------------------\n")
        print(Fore.CYAN + f"-------------------------------------ETAPE 2---------------------------------------  \n "
                          f"Choisissez un produit parmi la liste ci-dessus avec l'identifiant. \n "
                          f"----------------------------------------------------------------------------------- \n")
        rep = input(Fore.GREEN + f">> [Entrez un identifiant] : ")
        print(Fore.RESET)

        if rep in id_product_list:
            self.find_substitute(rep)
        elif rep.upper() == "M":
            self.display_menu()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print(Fore.RED + "OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
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
            self.cursor.execute(sql.USE_DATABASE)
            self.cursor.execute(sql.SELECT_SUBSTITUTES_BY_PRODUCT, (input_product_id,))
            result = self.cursor.fetchall()

            print(Fore.MAGENTA + f"  -----------------------------------------------------------------------  \n "
                                 f"                           LISTE DE SUBSTITUTS \n "
                                 f"------------------------------------------------------------------------- ")
            print(Fore.RESET)

            # Prints each substitute from list
            for substitute in result:
                print(f"________________________\n"
                      f"IDENTIFIANT: {substitute[4]}\n"
                      f"NOM SUBSTITUT: {substitute[5]}\n"
                      f"NUTRISCORE: {substitute[6]}\n")

            # Handles chosen substitute
            print(Fore.YELLOW + f"-----------------------AUTRES OPTIONS----------------------- \n"
                                f"[M] Retour au menus principal || [Q] Quitter le programme.   |\n"
                                f"------------------------------------------------------------\n")
            print(
                Fore.CYAN + f"-------------------------------------ETAPE 2---------------------------------------  \n "
                            f"Choisissez un substitut parmi la liste ci-dessus pour afficher plus de détails. \n "
                            f"----------------------------------------------------------------------------------- \n")
            rep = input(Fore.GREEN + f">> [Entrez un identifiant] : ")
            print(Fore.RESET)

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
                print(Fore.RED + "OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                                 "...")
                self.find_substitute(input_product_id)

        except mc.Error as err:
            print(f"Erreur lors de la sélection de substituts. Détails de l'erreur : {err}")

    def display_substitute(self, rep):
        """Method that displays the chosen substitute"""
        self.connect()

        try:
            self.cursor.execute(sql.USE_DATABASE)
            self.cursor.execute(sql.SELECT_SUBSTITUTE, (rep,))
            chosen_substitute = self.cursor.fetchone()

            # Finds substitute's store(s)
            self.cursor.execute(sql.SELECT_STORE, (rep,))
            store_substitute = [''.join(store) for store in self.cursor.fetchall()]  # fetchall returns a list of stores_substitute

            print(Fore.MAGENTA + f"______________________________________________________________\n"
                  f"Voici les détails du substitut choisi :")
            print(Fore.RESET)
            print(f"IDENTIFIANT........: {chosen_substitute[0]}\n"
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
            print(f"Erreur lors de l'affichage des détails du substitut. Détails de l'erreur : {err}")

        self.listen_choice_four(self.favorite)

    def listen_choice_four(self, favorite):
        print(Fore.CYAN + f"\n----------------ETAPE 4-------------------\n"
                          f"Que souhaitez-vous faire ?\n\n"
                          f"[S] - Sauvegarder le substitut.\n"
                          f"(M] - Retour au menus principal.\n"
                          f"[Q] - Quitter le programme.\n"
                          f"-----------------------------------------------\n")
        rep = input(Fore.GREEN + f">> [Entrez un identifiant] : ")
        print(Fore.RESET)

        if rep.upper() == "S":
            fm = FavoriteManager()
            fm.insert_favorite(favorite)
            print(Fore.MAGENTA + f"Votre substitut a été sauvegardé dans vos favoris.")
            print(Fore.RESET)
            self.display_menu()
        elif rep.upper() == "M":
            self.display_menu()
        elif rep.upper() == "Q":
            self.quit_program()
        else:
            print(Fore.RED + "OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                             "...")
            print(Fore.RESET)
            self.listen_choice_four(favorite)

    def display_favorite(self):
        """
        Method that displays all the favorite substitutes from favorite table
        """
        self.connect()
        try:
            self.cursor.execute(sql.USE_DATABASE)
            self.cursor.execute(sql.SELECT_FAVORITE)
            favorite_list = self.cursor.fetchall()

            print(Fore.MAGENTA + f"  -----------------------------------------------------------------------  \n "
                                 f"                   LISTE DE SUBSTITUTS ENREGISTRES\n "
                                 f"------------------------------------------------------------------------- \n")
            print(Fore.RESET)

            for favorite in favorite_list:
                print(f"________________________\n"
                      f"IDENTIFIANT........: {favorite[0]}\n"
                      f"NOM SUBSTITUT......: {favorite[1]}\n"
                      f"NUTRISCORE.........: {favorite[2]}\n"
                      f"CODE BARRE.........: {favorite[3]}\n"
                      f"MARQUE.............: {favorite[4]}\n"
                      f"URL................: {favorite[5]}\n"
                      f"LIEU(X) DE VENTE...: {favorite[6]}")

            self.disconnect()
        except mc.Error as err:
            print(f"Erreur lors de la sélection des substituts enregistrés. Détails de l'erreur : {err}")

    def quit_program(self):
        """ quitter le program quand appelée"""
        print(Fore.RED + f"------------------------------------------------- \n"
                         "OK, on arrête tout. C'est l'heure de la sieste.\n"
                         "A bientôt ! \n"
                         "zzZZZzz....................")
