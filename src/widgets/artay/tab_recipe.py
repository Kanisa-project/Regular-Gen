# import random
import random
from tkinter import *
from tkinter import ttk

from . import artstyle
from src.widgets.artay.recipe import rtabMarinades, rtabOSRS, rtabCasseroles, rtabSauces, \
    rtabSeasonings, rtabOther, rtabSandwiches, rtabSoups
from .recipe import rtabDesserts
from ...features.artay import recipe


# akt16 = ImageFont.truetype(os.getcwd() + "/assets/Fonts/Akt-Medium.ttf", 16)
# akt32 = ImageFont.truetype(os.getcwd() + "/assets/Fonts/Akt-Medium.ttf", 32)


class AlaNFT(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        """
        A tab to add a recipe on the kinvow with the help of the wordies tab.
        :param master: aRtay frame, housing all the other artay.
        :param IDUTC: idutc frame, user input frame.
        :param TEXIOTY: Texioty frame, for textual input and output
        :param KINVOW: Kinvow frame, for visual input(eventually) and output.
        """
        super(AlaNFT, self).__init__(master=master, width=width, height=height)
        self.osrsTab = None
        self.tab_name = "Recipe"

        self.recipeBook = ttk.Notebook(master=self)

        self.othersTab = rtabOther.Other(master=self.recipeBook, width=width, height=height)
        self.saucesTab = rtabSauces.Sauce(master=self.recipeBook, width=width, height=height)
        self.sandwichesTab = rtabSandwiches.Sandwich(master=self.recipeBook, width=width, height=height)
        self.soupsTab = rtabSoups.Soup(master=self.recipeBook, width=width, height=height)
        self.marinadesTab = rtabMarinades.Marinade(master=self.recipeBook, width=width, height=height)
        self.seasoningsTab = rtabSeasonings.Seasoning(master=self.recipeBook, width=width, height=height)
        self.dessertsTab = rtabDesserts.Dessert(master=self.recipeBook, width=width, height=height)
        self.casserolesTab = rtabCasseroles.Casserole(master=self.recipeBook, width=width, height=height)

        self.recipeBook.add(self.othersTab, text="Others")
        self.recipeBook.add(self.saucesTab, text="Sauces")
        self.recipeBook.add(self.sandwichesTab, text="Sandwiches")
        self.recipeBook.add(self.soupsTab, text="Soups")
        self.recipeBook.add(self.marinadesTab, text="Marinades")
        self.recipeBook.add(self.seasoningsTab, text="Seasonings")
        self.recipeBook.add(self.dessertsTab, text="Desserts")
        self.recipeBook.add(self.casserolesTab, text="Casseroles")
        self.recipeBook.grid(column=0, row=0)

        self.chosen_recipe_dict = {}

    def add_osrs_tab(self):
        self.osrsTab = rtabOSRS.OSRS(master=self.recipeBook)
        self.recipeBook.add(self.osrsTab, text="OSRS")
        # print("added")

    def gather_recipe_options(self) -> dict:
        chosen_recipe_options = self.chosen_recipe_dict
        print(chosen_recipe_options)
        return chosen_recipe_options

    def gather_random_options(self) -> dict:
        ran_category = random.choice(["Casseroles", "Sauces", "Soups", "Desserts", "Sandwiches", "Seasonings"])
        recipe_dict = {
            "Casseroles": rtabCasseroles.RECIPES_DICT,
            "Sauces": rtabSauces.RECIPES_DICT,
            "Soups": rtabSoups.RECIPES_DICT,
            "Desserts": rtabDesserts.RECIPES_DICT,
            "Sandwiches": rtabSandwiches.RECIPES_DICT,
            "Seasonings": rtabSeasonings.RECIPES_DICT
        }
        ran_recipe = random.choice(list(recipe_dict[ran_category].keys()))
        chosen_recipe_options = recipe_dict[ran_category][ran_recipe]
        return chosen_recipe_options

    def add_recipe(self, img: Image, kre8dict: dict, abt='masterpiece') -> Image:
        recipe.add_ingredients(img, kre8dict)
        recipe.add_directions(img, kre8dict)
        recipe.add_labels(img, kre8dict)
        return img

    def command_recipe(self, command_arg) -> dict:
        category = command_arg.title()
        recipe_dict = {
            "Casseroles": rtabCasseroles.RECIPES_DICT,
            "Sauces": rtabSauces.RECIPES_DICT,
            "Soups": rtabSoups.RECIPES_DICT,
            "Desserts": rtabDesserts.RECIPES_DICT,
            "Sandwiches": rtabSandwiches.RECIPES_DICT,
            "Seasonings": rtabSeasonings.RECIPES_DICT,
            "Other": rtabOther.RECIPES_DICT
        }
        ran_recipe = random.choice(list(recipe_dict[category].keys()))
        chosen_recipe_options = recipe_dict[category][ran_recipe]
        return chosen_recipe_options
