import recipeTab

RECIPES_DICT = {
    "Beef Shtoe": {
        "recipe_info": ["Foreplay", "Beef Shtoe"],
        "ingredients": {
            "Potatoes": ["7"],
            "Carrots": ["5"],
            "Onions": ["2"],
            "Old Shoe": ["1"],
            "Beef": ["4lbs"],
            "Garlic cloves": ["3"]
        },
        "directions": {
            "Step 1": "Boil water.",
            "Step 2": "Add food.",
            "Step 3": "Wait 6 hours.",
            "Step 4": "Beef shtoe."
        }
    }
}


class Soup(recipeTab.Recitab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(list(RECIPES_DICT.keys()))
        self.button_dict["Beef Shtoe"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Beef Shtoe"]))
