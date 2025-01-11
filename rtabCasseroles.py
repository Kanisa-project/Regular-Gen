import recipeTab

RECIPES_DICT = {
    "Scalloped Taters": {
        "recipe_info": ["Megan", "Scalloped Taters"],
        "ingredients": {
            "Thin sliced taters": ["4c"],
            "Butter": ["3tbsp"],
            "Flour": ["3tbsp"],
            "Milk": ["1-1/2c"],
            "Salt": ["1tsp"],
            "Cayenne": ["⚝"],
            "Cheddar Cheese": ["1-1/2c"]
        },
        "directions": {
            "Step 1": "Preheat oven 350; Grease 1.5 qrt 9x9 pan.",
            "Step 2": "Melt butter in small sauce pan and stir in flour.",
            "Step 3": "Whisk in milk very slowly, season with salt and cayenne.",
            "Step 4": "Cook on low until smooth and boiling, occasionally stir with whisk.",
            "Step 5": "Reduce heat and stir in cheese.",
            "Step 6": "Place half the potatoes in baking dish and pour half of sauce.",
            "Step 7": "Place other half the potatoes in baking dish and pour other half of sauce.",
            "Step 8": "Sprinkle 1/2 cup cheese on top and back for an hour until potatoes are done."
        }
    }
}


class Casserole(recipeTab.Recitab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(list(RECIPES_DICT.keys()))
        self.button_dict["Scalloped Taters"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Scalloped Taters"]))
