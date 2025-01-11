import recipeTab

RECIPES_DICT = {
    'None Bread': {
        "recipe_info": ["Me", 'None Bread'],
        "ingredients": {
            "Nothing": ["1cup"],
            "Nada": ["1T"],
            "Zilch": ["1/2cup"]

        },
        "directions": {
            "Step 0": "Put nothing in a bag with nada.",
            "Step nope": "Seal the bag and shake violently.",
            "Step 00": "Place in microwave with zilch for\n 22 minutes.",
            "Step never": "Form into loaf ball and set on sidewalk.",
        }
    },
    'Blank Sandwich': {
        "recipe_info": ["Me", 'Blank Sandwich'],
        "ingredients": {
            "None Bread": ["2 slices"],
            "Nan": ["1/2cup"]

        },
        "directions": {
            "Step 0": "Put nothing between the None Breads.",
            "nope": "Flip sandwich upside down",
            "Step 00": "Add NaN and 404.",
        }
    }
}


class Other(recipeTab.Recitab):
    def __init__(self, master=None):
        super().__init__(master=master)
        recipe_name_list = list(RECIPES_DICT.keys())
        self.setup_button_choices(recipe_name_list)
        self.button_dict["None Bread"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["None Bread"]))
        self.button_dict["Blank Sandwich"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Blank Sandwich"]))
