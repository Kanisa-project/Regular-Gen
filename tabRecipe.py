# import random
import random
from tkinter import *
from tkinter import ttk

from PIL import ImageFont, ImageDraw

import artstyle
import recipe
import rtabCasseroles
import rtabDesserts
import rtabMarinades
import rtabOSRS
import rtabOther
import rtabSandwiches
import rtabSauces
import rtabSeasonings
import rtabSoups

emonob16 = ImageFont.truetype("emonob.ttf", 16)
emonob32 = ImageFont.truetype("emonob.ttf", 32)


class AlaNFT(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        """
        A tab to add a recipe on the kinvow with the help of the wordies tab.
        :param master: aRtay frame, housing all the other artyles.
        :param IDUTC: idutc frame, user input frame.
        :param TEXIOTY: Texioty frame, for textual input and output
        :param KINVOW: Kinvow frame, for visual input(eventually) and output.
        """
        super(AlaNFT, self).__init__(master=master, idutc=idutc, width=width, height=height)
        self.osrsTab = None
        self.tab_name = "recipe"

        self.recipeBook = ttk.Notebook(master=self)

        self.othersTab = rtabOther.Other(master=self.recipeBook)
        self.saucesTab = rtabSauces.Sauce(master=self.recipeBook)
        self.sandwichesTab = rtabSandwiches.Sandwich(master=self.recipeBook)
        self.soupsTab = rtabSoups.Soup(master=self.recipeBook)
        self.marinadesTab = rtabMarinades.Marinade(master=self.recipeBook)
        self.seasoningsTab = rtabSeasonings.Seasoning(master=self.recipeBook)
        self.dessertsTab = rtabDesserts.Dessert(master=self.recipeBook)
        self.casserolesTab = rtabCasseroles.Casserole(master=self.recipeBook)

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
        print("added")

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
            "Seasonings": rtabSeasonings.RECIPES_DICT,
        }
        ran_recipe = random.choice(list(recipe_dict[ran_category].keys()))
        chosen_recipe_options = recipe_dict[ran_category][ran_recipe]
        return chosen_recipe_options

    def add_recipe(self, img: Image, kre8dict: dict, abt='masterpiece') -> Image:
        recipe.add_ingredients(img, kre8dict)
        recipe.add_directions(img, kre8dict)
        recipe.add_labels(img, kre8dict)
        return img
