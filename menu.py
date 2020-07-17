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
        """ print() et input() between:
        1 - Quel aliment souhaitez-vous remplacer ?
        2 - Retrouver mes aliments substitués.
        3 - Quitter le programme.

        si input(1) : run find_categories_to_display()
        si input(2) : ... ?
        si input(3) : quit_program()
        """

        b = "OK retrouvons les substituts enregistrés dans la table substitute..."

        print(f" ------------------------------------------ \n"
              f"MENU PRINCIPAL : Que souhaitez-vous faire ?\n "
              f"------------------------------------------ \n")

        rep = input(f"[1] - Rechercher un substitut à un aliment. \n"
                    f"[2] - Retrouver mes aliments substitués. \n"
                    f"[Q] - Quitter le programme.\n")

        if rep == "1":
            self.find_display_categories()
        elif rep == "2":
            print(b)
        elif rep == "Q":  # elif rep == "Q" or "q":
            self.quit_program()
        else:
            print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                  "...")
            self.display_menu()

    def find_display_categories(self):
        """find randomly 10 categories from category table
        + display them
        + print() et input() between:
        1 - Sélectionnez la catégorie.
        2 - Quitter le programme.

        si input(entre 1 et 10) : find_display_products()
        si input("2") quit_program()"""
        cnx = self.cnx
        cursor = self.cursor
        self.connect()

        try:
            cursor.execute(sql_queries.USE_DATABASE)
            cursor.execute(sql_queries.SELECT_CATEGORY_WITH_UNHEALTHY_PRODUCTS)
            result = cursor.fetchall()

            print(f" ------------------------------------------------------------- \n "
                  f"Veuillez sélectionner une catégorie parmi la liste suivante : \n "
                  f"------------------------------------------------------------- \n")
            for category in result:
                print(f"\n {category}")

            cursor.close()
            cnx.close()
        except mc.Error as err:
            print(f"Unsuccessful selection of categories with unhealthy products: {err}")

        self.display_question_two()

    def display_question_two(self):
        print(f" ------------------------- \n"
              f"Que souhaitez-vous faire ?\n "
              f"------------------------- \n")

        rep = input(f"(M] - Retour au menu principal.\n"
                    f"[Q] - Quitter le programme.\n")

        if rep == "1":
            pass
        elif rep == "M":  # elif rep == "M" or "m":
            self.display_menu()
        elif rep == "Q":  # elif rep == "Q" or "q":
            self.quit_program()
        else:
            print("OUPS ! Je n'ai pas compris votre choix... Et si on réessayait? \n"
                  "...")
            self.display_question_two()

    def find_display_products_by_category(self):
        """
        find 5 random produits correspondants à categorie
        + afficher/display
        + print() et input() between:
        si input(entre 1 et 5) : find_substitute()
        si input("2") quit_program()

        """
        pass

    def find_substitute(self):
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
