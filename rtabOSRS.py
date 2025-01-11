import recipeTab

RECIPES_DICT = {
    'Toad Crunchies': {
        "recipe_info": ["Jagex(Gnomes)", "Toad Crunchies", "Food"],
        "ingredients": {
            "Equa Leaves": ["1"],
            "Gianne Dough": ["1"],
            "Gnome Spice": ["1"],
            "Toad's legs": ["2sets"]
        },
        "directions": {
            "Step 1": "Gianne dough goes inside crunchy tray.",
            "Step 2": "Bake the dough into crunchies.",
            "Step 3": "Add toad legs and gnome spice.",
            "Step 4": "Finish baking the crunchies.",
            "Step 5": "Add the equa leaves on top for garnish."
        }
    },
    'Worm Batta': {
        "recipe_info": ["Jagex(Gnomes)", "Worm Batta", "Food"],
        "ingredients": {
            "Equa Leaves": ["1"],
            "Gianne Dough": ["1"],
            "Cheese": ["1"],
            "Gnome Spice": ["1"],
            "King worm": ["1"]
        },
        "directions": {
            "Step 1": "Gianne dough goes inside batta tin.",
            "Step 2": "Bake the dough to lightly brown.",
            "Step 3": "Add king worm, gnome spice and cheese.",
            "Step 4": "Bake until cheese is melted or you smell the worm.",
            "Step 5": "Add the equa leaves on top for garnish."
        }
    },
    'Wizard Blizzard': {
        "recipe_info": ["Jagex(Gnomes)", "Wizard Blizzard", "Drink"],
        "ingredients": {
            "Vodka": ["2parts"],
            "Gin": ["1part"],
            "Lime": ["1", "juice"],
            "Lime slice": ["1"],
            "Lemon": ["1", "juice"],
            "Orange": ["1", "juice"],
            "Pineapple chunks": ["1"]
        },
        "directions": {
            "Step 1": "Add vodka, gin, lime, lemon, and orange juice to cocktail shaker.",
            "Step 2": "Shake shake shake.",
            "Step 3": "Pour into cocktail glass.",
            "Step 4": "Add pineapple chunks and lime slice for garnish."
        }
    },
    'Blurberry Special': {
        "recipe_info": ["Jagex(Gnomes)", "Blurberry Special", "Drink"],
        "ingredients": {
            "Vodka": ["1part"],
            "Brandy": ["1part"],
            "Gin": ["1part"],
            "Lemon": ["2", "juice"],
            "Orange": ["1", "juice"],
            "Lemon chunks": ["1"],
            "Orange chunks": ["1"],
            "Equa leaves": ["1"],
            "Lime sliced": ["1"]
        },
        "directions": {
            "Step 1": "Add vodka, brandy, gin, lemon, and orange to cocktail shaker.",
            "Step 2": "Shake shake shake.",
            "Step 3": "Pour into cocktail glass.",
            "Step 4": "Add lemon and orange chunks.",
            "Step 5": "Garnish with equa leaves and sliced lime."
        }
    },
}


class OSRS(recipeTab.Recitab):
    def __init__(self, master=None):
        super().__init__(master=master)
        recipe_name_list = list(RECIPES_DICT.keys())
        self.setup_button_choices(recipe_name_list)
        self.button_dict["Toad Crunchies"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Toad Crunchies"]))
        self.button_dict["Worm Batta"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Worm Batta"]))
        self.button_dict["Wizard Blizzard"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Wizard Blizzard"]))
        self.button_dict["Blurberry Special"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Blurberry Special"]))
