import recipeTab

RECIPES_DICT = {
    "Graham Cracker Crust": {
        "recipe_info": ["Megan", "Graham Cracker Crust"],
        "ingredients": {
            "Graham Cracker Crumbs": ["1.5c"],
            "Sugar": ["1/4c"],
            "Unsalted Butter, melted": ["6tbsp"]
        },
        "directions": {
            "Step 1": "Stir crumbs and sugar together.",
            "Step 2": "Stir in melted butter.",
            "Step 3": "Shape into pie pan."
        }
    },
    "Chocolate Eclairs": {
        "recipe_info": ["Nana", "Chocolate Eclairs"],
        "ingredients": {
            "Graham Crackers": ["2.5 pkg"],
            "Banana pudding": ["1 box"],
            "Vanilla pudding": ["1 box"],
            "Chocolate topping": ["2c"]
        },
        "directions": {
            "Step 1": "Graham crackers and mixed puddings in a lasagna style.",
            "Step 2": "Graham crackers on top and then chocolate sauce on top of that.",
            "Step 3": "Let set over night."
        }
    }
}


class Dessert(recipeTab.Recitab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(list(RECIPES_DICT.keys()))
        self.button_dict["Graham Cracker Crust"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Graham Cracker Crust"]))
        self.button_dict["Chocolate Eclairs"][1].configure(command=lambda: self.set_used_recipe(RECIPES_DICT["Chocolate Eclairs"]))
