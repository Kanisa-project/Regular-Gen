import recipeTab


RECIPES_DICT = {
    'Jalaturkeypeno': {
        "recipe_info": ["DJ Spray", 'Jalaturkeypeno'],
        "ingredients": {
            "Turkey": ["3 slices"],
            "Cream Cheese": ["1T"],
            "Mayonnaise": ["⚝"],
            "Mustard": ["⚝"],
            "Provolone Cheese": ["1 slice"],
            "Cheddar Jalapeno Bagel": ["two halves"]

        },
        "directions": {
            "Step 1": "Toast the bagel then spread your condiments on.",
            "Step 2": "Add the provolone cheese and turkey.",
            "Step 3": "Sandwich together and enjoy.",
        }
    },
    'PBJ': {
        "recipe_info": ["DJ Spray", 'PBJ'],
        "ingredients": {
            "Peanut butter": ["2TBSP"],
            "Grape jelly": ["2TBSP"],
            "Bread": ["2 slices"]

        },
        "directions": {
            "Step 1": "Spread peanut butter on one slice of bread.",
            "Step 2": "Spread jelly on other slice of bread.",
            "Step 3": "Sandwich together and enjoy.",
        }
    }
}


class Sandwich(recipeTab.Recitab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(list(RECIPES_DICT.keys()))
        self.button_dict["Jalaturkeypeno"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Jalaturkeypeno"]))
        self.button_dict["PBJ"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["PBJ"]))
