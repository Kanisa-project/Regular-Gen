import recipeTab

RECIPES_DICT = {
    "Cranberry Sauce": {
        "recipe_info": ["Megan", "Cranberry Sauce"],
        "ingredients": {
            "Cranberries": ["3c", "set aside 1c"],
            "Sugar": ["1c"],
            "Orange or Lemon Zest": ["⚝"],
            "Water": ['4tbsp']
        },
        "directions": {
            "Step 1": "Combine all ingredients into sauce pan, cook on low heat",
            "Step 2": "Stir occasionally until sugar dissolves and cranberries are soft. About 10 minutes.",
            "Step 3": "Increase heat to medium and cook until cranberries burst. About 12 minutes.",
            "Step 4": "Reduce heat to low and stir in reserved berries."
        }
    },
    "Fancy Mustard": {
        "recipe_info": ["DJspray", "Fancy Mustard"],
        "ingredients": {
            "Ketchup": ["2T"],
            "Mustard": ["2T"],
            "Mayonnaise": ["1T"],
            "Malt Vinegar": ["1T"],
            "Cholula": ["1T"],
            "Honey": ["1tsp"]
        },
        "directions": {
            "Step 1": "Mix it all together.",
            "Step 2": "Dip fried foods in it."
        }
    },
    "Unnamed Sauce": {
        "recipe_info": ["Junior", "Unnamed Sauce"],
        "ingredients": {
            "BBQ sauce": ["1cup"],
            "Whiskey": ["1cup"],
            "Frank's redhot": ["1cup"],
            "chipotle": ["1/2cup", "can"],
            "dijon": ["1cup"],
            "Sweet chili": ["3/2cup"],
            "Pineapple juice": ["4oz"]
        },
        "directions": {
            "Step 1": "Flambe the whiskey.",
            "Step 2": "Mix it all together in a bowl.",
            "Step 3": "Eat with spoon or straw."
        }
    },
}


class Sauce(recipeTab.Recitab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(list(RECIPES_DICT.keys()))
        self.button_dict["Cranberry Sauce"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Cranberry Sauce"]))
        self.button_dict["Fancy Mustard"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Fancy Mustard"]))
        self.button_dict["Unnamed Sauce"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Unnamed Sauce"]))
