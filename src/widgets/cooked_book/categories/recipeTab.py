from tkinter import StringVar, Label, Button, Entry
from tkinter.ttk import Frame
from src.widgets.tabbed_widget import TabbedWidget

RECIPES_DICT = {}


class Recitab(TabbedWidget):
    def __init__(self, width, height, master=None, text="Recipe"):
        super().__init__(width, height, master, text)
        self.tab_name = "Reciptab"
        self.labels_dict = {}

        self.chosen_options_dict = {}
        self.widget_display_array = []
        self.setup_labels(["ingredients:"], start_x_cell=5, start_y_cell=0)
        self.setup_labels(["directions:"], start_x_cell=5, start_y_cell=6)

    def set_used_recipe(self, recipe_dict: dict) -> dict:
        self.master.master.chosen_recipe_dict = recipe_dict
        self.delete_text_boxes()
        self.setup_ingredient_text_boxes(recipe_dict["ingredients"], start_x_cell=6, start_y_cell=0)
        self.setup_direction_text_boxes(recipe_dict["directions"], start_x_cell=6, start_y_cell=6)
        return recipe_dict


    def delete_text_boxes(self):
        for textbox in self.textbox_dict:
            self.textbox_dict[textbox][2].destroy()
            self.textbox_dict[textbox][3].destroy()
        self.textbox_dict = {}

    def setup_labels(self, word_list: list, start_x_cell: int, start_y_cell: int):
        """
        Set up a dictionary of labels for the given word_list.
        :param start_y_cell:
        :param start_x_cell:
        :param word_list: List of words to use as labels.
        :return:
        """
        if word_list in self.widget_display_array:
            print("already done in")
        else:
            self.widget_display_array.append(word_list)
        for i, word in enumerate(word_list):
            str_var = StringVar(value=word)
            label = Label(self, textvariable=str_var)
            self.labels_dict[word] = [str_var, label]
            row = i % 10
            col = i // 10
            label.grid(column=col+start_x_cell, row=row+start_y_cell)

    def setup_ingredient_text_boxes(self, ingredient_dict: dict, start_x_cell=0, start_y_cell=0):
        for i, (key, value) in enumerate(ingredient_dict.items()):
            amt_var = StringVar(value=f"{value[0]}")
            ing_var = StringVar(value=f"{key}")
            amt_entry = Entry(self, textvariable=amt_var, width=4)
            ing_entry = Entry(self, textvariable=ing_var, width=12)
            self.textbox_dict[f"I{i}"] = [amt_var, ing_var, amt_entry, ing_entry]
            row = i % 5
            col = i % 5
            if i > 4:
                col += 2 + start_x_cell
                if i > 9:
                    col += 2 + start_x_cell
            amt_entry.grid(column=col-i+start_x_cell, row=row+start_y_cell)
            ing_entry.grid(column=col+1-i+start_x_cell, row=row+start_y_cell)

    def setup_direction_text_boxes(self, direction_dict: dict, start_x_cell=0, start_y_cell=0):
        for i, (key, value) in enumerate(direction_dict.items()):
            step_var = StringVar(value=f"{key}")
            dir_var = StringVar(value=f"{value}")
            step_entry = Entry(self, textvariable=step_var, width=5)
            dir_entry = Entry(self, textvariable=dir_var, width=55)
            row = i % 10
            col = i // 10
            step_entry.grid(column=col+start_x_cell, row=row+start_y_cell)
            dir_entry.grid(column=col+1+start_x_cell, row=row+start_y_cell, columnspan=8)
