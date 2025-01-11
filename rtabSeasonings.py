import recipeTab

RECIPES_DICT = {
    "BBQ Seasoning": {
        "recipe_info": ["Junior", "BBQ Seasoning"],
        "ingredients": {
            "Brown Sugar": ["1cup"],
            "Paprika": ["1T"],
            "Cayenne": ["1tsp"],
            "Chili Powder": ["1T"],
            "Mustard Powder": ["1T"],
            "Onion Powder": ["1T"],
            "Garlic Powder": ["1T"],
            "Salt": ["⚝"],
            "Pepper": ["⚝"],
            "Parsley": ["1T", "dry"],
            "Oregano": ["1T", "dry"]
        },
        "directions": {
            "Step 1": "Mix it all together.",
            "Step 2": "Sprinkle and not rub it onto the meat.",
            "Step 3": "Cook the meat.",
        }
    },
}


class Seasoning(recipeTab.Recitab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(list(RECIPES_DICT.keys()))
        self.button_dict["BBQ Seasoning"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["BBQ Seasoning"]))

