import recipeTab


RECIPES_DICT = {
    'Chimichurri': {
        "recipe_info": ["Junior", "Chimichurri"],
        "ingredients": {
            "Olive Oil": ["3T"],
            "Redwine Vinaigrette": ["1T"],
            "Parsley": ["⚝"],
            "Garlic": ["⚝"],
            "Red Chili": ["⚝"],
            "Oregano": ["⚝"],
            "Salt": ["⚝"],
            "Pepper": ["⚝"],
            "Red Onion": ["⚝"],
            "Lemon Juice": ["⚝"]
        },
        "directions": {
            "Step 1": "Chop stuff and mix it.",
            "Step 2": "Good for dipping?"
        }
    },
    "Lamb Marinade": {
        "recipe_info": ["Junior", "Lamb Marinade"],
        "ingredients": {
            "Red Wine": ["1cup"],
            "Redwine Vinaigrette": ["1cup"],
            "Olive Oil": ["3T"],
            "Rosemary": ["⚝"],
            "Garlic": ["⚝"],
            "Salt": ["⚝"],
            "Pepper": ["⚝"],
            "Red Onion": ["⚝"],
            "Mustard": ["⚝"]
        },
        "directions": {
            "Step 1": "Mix it all together.",
            "Step 2": "Marinade the lamb.",
            "Step 3": "Cook the lamb.",
            "Step 4": "Eat the lamb."
        }
    },
    "Poke Marinade": {
        "recipe_info": ["Junior", "Poke Marinade"],
        "ingredients": {
            "Soy Sauce": ["1cup"],
            "Sesame Oil": ["2T"],
            "Toasted Sesame": ["1T"],
            "Green Onions": ["1/4cup"],
            "Red Peppers": ["1tsp"],
            "Garlic": ["1tsp", "minced"],
            "Ginger": ["1tsp", "minced"],
            "Onion": ["1T", "minced"],
            "Sriracha": ["⚝"]
        },
        "directions": {
            "Step 1": "Mix it all together.",
            "Step 2": "Marinade the poke.",
            "Step 3": "Cook the poke.",
            "Step 4": "Eat the poke."
        }
    }
}


class Marinade(recipeTab.Recitab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(list(RECIPES_DICT.keys()))
        self.button_dict["Chimichurri"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Chimichurri"]))
        self.button_dict["Lamb Marinade"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Lamb Marinade"]))
        self.button_dict["Poke Marinade"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Poke Marinade"]))
