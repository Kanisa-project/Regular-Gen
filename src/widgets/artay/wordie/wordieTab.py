from tkinter import StringVar, Label

from src.widgets.tabbed_widget import TabbedWidget

RECIPES_DICT = {}


class Wordietab(TabbedWidget):
    def __init__(self, width, height, master=None, text="Wordie"):
        super().__init__(width, height, master, text)
        self.tab_name = "Wordietab"
        self.labels_dict = {}
        self.label_group_names = []

    def setup_labels(self, word_list: list, group_name="default", start_x_cell=0, start_y_cell=0):
        """
        Set up a dictionary of labels for the given word_list.
        :param group_name:
        :param start_y_cell:
        :param start_x_cell:
        :param word_list: List of words to use as labels.
        :return:
        """
        if group_name not in self.label_group_names:
            self.labels_dict[group_name] = {}
            self.label_group_names.append(group_name)
            print(self.label_group_names)

        for i, word in enumerate(word_list):
            str_var = StringVar(value=word)
            label = Label(self, textvariable=str_var)
            self.labels_dict[group_name][word] = [str_var, label]
            row = i % 10
            col = i // 10
            label.grid(column=col + start_x_cell, row=row + start_y_cell)

    def update_labels(self, word_list: list, group_name="default"):
        for i, word_lbl in enumerate(self.labels_dict[group_name]):
            print(self.labels_dict)
            self.labels_dict[group_name][word_lbl][0].set(word_list[i])
            print("updating", word_lbl)
