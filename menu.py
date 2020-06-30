"""Module that handles the app menu"""


class Menu:

    def __init__(self):
        self.display_menu()

    def display_menu(self):
        """ print() et input() between:
        1 - Quel aliment souhaitez-vous remplacer ?
        2 - Retrouver mes aliments substitués.
        3 - Quitter le programme.

        si input(1) : run find_categories_to_display()
        si input(2) : ... ?
        si input(3) : quit_program()
        """
        a = "OK lançons la méthode :find_display_categories..."
        b = "OK retrouvons les substituts enregistrés dans la table substitute..."

        print(f"Que souhaitez-vous faire ?")

        rep = input(f"1 - Rechercher un substitut à un aliment. \n"
                    f"2 - Retrouver mes aliments substitués. \n"
                    f"3 - Quitter le programme.")

        if rep == "1":
            print(a)
        elif rep == "2":
            print(b)
        elif rep == "3":
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
        pass

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
        print("OK, on arrête tout. C'est l'heure de la sieste.\n"
              "A bientôt ! \n"
              "zzZZZzz...")


menu = Menu()
