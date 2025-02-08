from tkinter import *
from settings import *
from tkinter import ttk
import artstyle

RECIPES_DICT = {}


class Wordietab(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.tab_name = "Worditab"
        self.checkbutton_dict = {}

        self.radiobutton_dict = {}

        self.textbox_dict = {}

        self.slider_dict = {}
        self.slider_limit_dict = {}

        self.button_dict = {}

        self.optionmenu_dict = {}

        self.dropdown_menu_dict = {}

        self.labels_dict = {}
        self.label_group_names = []

        self.chosen_options_dict = {}
        self.widget_display_array = []

    def set_used_wordie(self, wordie_dict: dict) -> dict:
        self.master.master.chosen_wordie_dict = wordie_dict
        print(self.master)
        self.delete_text_boxes()
        # self.setup_ingredient_text_boxes(wordie_dict["ingredients"], start_x_cell=6, start_y_cell=0)
        # self.setup_direction_text_boxes(wordie_dict["directions"], start_x_cell=6, start_y_cell=6)
        return wordie_dict

    # def update_slider_label(self, intvar, strvar) -> str:
    #     strvar.set(intvar.get())
    #     return str(self.widget_display_array)

    def delete_text_boxes(self):
        for textbox in self.textbox_dict:
            self.textbox_dict[textbox][2].destroy()
            self.textbox_dict[textbox][3].destroy()
        self.textbox_dict = {}

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

        # if word_list in self.widget_display_array:
        #     print("already done in")
        # else:
        #     self.widget_display_array.append(word_list)
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

    def setup_text_boxes(self, keyed_dict: dict, start_x_cell=0, start_y_cell=0, width=10):
        """
        Set up a specified number of text boxes on the artyle tab.

        :param keyed_dict:
        :param width:
        :param start_y_cell:
        :param start_x_cell:
        """
        for i, word in enumerate(keyed_dict):
            lbl_str = StringVar(value=word + ": ")
            lbl = Label(self, textvariable=lbl_str)
            str_var = StringVar(value=keyed_dict[word])
            entry = Entry(self, textvariable=str_var, width=width)
            self.textbox_dict[word] = [str_var, entry]
            row = (i % 5)
            col = (i // 5 + 1)
            lbl.grid(column=col + start_x_cell - 1, row=row + start_y_cell, sticky='e')
            entry.grid(column=col + start_x_cell, row=row + start_y_cell, columnspan=2)

    # def setup_text_boxes(self, word_list: list, start_x_cell=0, start_y_cell=0, width=10, textbox_name=""):
    #     """
    #     Set up a specified number of text boxes on the artyle tab.
    #
    #     :param textbox_name:
    #     :param width:
    #     :param start_y_cell:
    #     :param start_x_cell:
    #     :param word_list:
    #     """
    #     if word_list in self.widget_display_array:
    #         pass
    #     else:
    #         self.widget_display_array.append(word_list)
    #         for i, word in enumerate(word_list):
    #             str_var = StringVar(value=word)
    #             entry = Entry(self, textvariable=str_var, width=width)
    #             key = f"{textbox_name}{i}"
    #             self.textbox_dict[key] = [str_var, entry]
    #
    #             row = (i % 5)
    #             col = (i // 5 + 1)
    #
    #             entry.grid(column=col + start_x_cell, row=row + start_y_cell)

    def setup_button_choices(self, button_list: list, start_x_cell=0, start_y_cell=0):
        """
        Set up buttons on the artyle tab.

        :param start_y_cell:
        :param start_x_cell:
        :param button_list: List of words for buttons to use.
        :return:
        """
        self.widget_display_array.append(button_list)
        for i, option in enumerate(button_list):
            str_var = StringVar(value=option)
            button = Button(self, textvariable=str_var)
            self.button_dict[option] = [str_var, button]

            row = (i % 10)
            col = (i // 10)

            button.grid(column=col + start_x_cell, row=row + start_y_cell)

    def setup_checkbutton_choices(self, word_list: list):
        """
        Set up checkbutton choices on the artyle tab.

        :param word_list: A list of words to be used as options.
        """
        self.widget_display_array.append(word_list)
        for i, option in enumerate(word_list):
            int_var = IntVar()
            str_var = StringVar(value=option)
            checkbutton = Checkbutton(self, text=option, variable=int_var)

            self.checkbutton_dict[option] = [int_var, str_var, checkbutton]

            row = (i % 10)
            col = (i // 10)

            checkbutton.grid(column=len(self.widget_display_array) + col, row=row)

    def destroy_word_optionmenus(self):
        """Destroy each of the optionmenus that contain wordlists"""
        for c in self.dropdown_menu_dict:
            self.dropdown_menu_dict[c][1].destroy()

    def setup_dropdown_menus(self, word_list=None, word_str=None, dropdown_name="", start_x_cell=0, start_y_cell=0):
        if word_str:
            self.widget_display_array.append(word_str)
            for c in word_str:
                while c in self.dropdown_menu_dict:
                    c += c
                words_str_var = StringVar(value=ALPHANUMERIC_WORD_LISTS[c[:1].lower()][0])
                self.dropdown_menu_dict[c] = [words_str_var,
                                              OptionMenu(self, words_str_var, *ALPHANUMERIC_WORD_LISTS[c[:1].lower()])]
        elif word_list:
            self.widget_display_array.append(dropdown_name)
            word_str_var = StringVar(value=word_list[0])
            self.dropdown_menu_dict[dropdown_name] = [word_str_var,
                                                      OptionMenu(self, word_str_var, *word_list)]

        for i, dropdown in enumerate(list(self.dropdown_menu_dict.keys())):
            row = i % 10
            col = i // 10
            self.dropdown_menu_dict[dropdown][1].grid(column=col + start_x_cell, row=row + start_y_cell)

    def setup_number_wheel(self, num_wheel_name: str, callback, start_x_cell=0, start_y_cell=0):
        self.widget_display_array.append(num_wheel_name)
        wheel_value = IntVar()
        self.dropdown_menu_dict[num_wheel_name] = [wheel_value,
                                                   ttk.OptionMenu(self, wheel_value, *list(range(-1, 10)),
                                                                  command=lambda num_boxes: callback(wheel_value.get()))]
        wheel_value.set(0)
        self.dropdown_menu_dict[num_wheel_name][1].grid(column=start_x_cell, row=start_y_cell)

    # def setup_slider_bars(self, slider_list: list):
    #     """
    #     Set up a dictionary of sliders for a given list of parameters.
    #
    #     :param slider_list: A list of parameter names.
    #     """
    #     self.widget_display_array.append(slider_list)
    #     for i, parameter in enumerate(slider_list):
    #         min_val, max_val = self.slider_limit_dict[parameter]
    #         str_var = StringVar(value=parameter + " : ")
    #         int_var = IntVar(value=(max_val + min_val) // 2)
    #         label = Label(self, textvariable=str_var)
    #         scale = Scale(self, from_=min_val, to=max_val, variable=int_var, width=5, length=88,
    #                       orient="horizontal", borderwidth=0, sliderlength=6, showvalue=False,
    #                       command=self.update_slider_label(int_var, str_var))
    #         self.slider_dict[parameter] = [int_var, str_var, scale, label]
    #         # scale.configure(command=self.update_slider_label)
    #
    #         row = i % 10
    #         col = i // 10
    #         scale.grid(column=len(self.widget_display_array) + col, row=row, sticky="se")
    #         label.grid(column=len(self.widget_display_array), row=row, sticky="nw")

    # def setup_radiobutton_choices(self, options_list: list):
    #     """
    #     Radio button choices setup.
    #     :param options_list: list of options for the radio buttons
    #     :return: None
    #     """
    #     int_var = IntVar()
    #     self.widget_display_array.append(options_list)
    #     for i, option in enumerate(options_list):
    #         new_str_var = StringVar(value=option)
    #         radiobutton = Radiobutton(self, text=option, variable=int_var, value=i)
    #         radiobutton.grid(column=len(self.widget_display_array) + 0, row=i)
    #         self.radiobutton_dict[option] = [int_var, new_str_var, radiobutton]

    # def setup_ingredient_text_boxes(self, ingredient_dict: dict, start_x_cell=0, start_y_cell=0):
    #     for i, (key, value) in enumerate(ingredient_dict.items()):
    #         amt_var = StringVar(value=f"{value[0]}")
    #         ing_var = StringVar(value=f"{key}")
    #         amt_entry = Entry(self, textvariable=amt_var, width=4)
    #         ing_entry = Entry(self, textvariable=ing_var, width=12)
    #         self.textbox_dict[f"I{i}"] = [amt_var, ing_var, amt_entry, ing_entry]
    #         row = i % 5
    #         col = i % 5
    #         if i > 4:
    #             col += 2 + start_x_cell
    #             if i > 9:
    #                 col += 2 + start_x_cell
    #         amt_entry.grid(column=col-i+start_x_cell, row=row+start_y_cell)
    #         ing_entry.grid(column=col+1-i+start_x_cell, row=row+start_y_cell)

    # def setup_direction_text_boxes(self, direction_dict: dict, start_x_cell=0, start_y_cell=0):
    #     for i, (key, value) in enumerate(direction_dict.items()):
    #         step_var = StringVar(value=f"{key}")
    #         dir_var = StringVar(value=f"{value}")
    #         step_entry = Entry(self, textvariable=step_var, width=5)
    #         dir_entry = Entry(self, textvariable=dir_var, width=55)
    #         row = i % 10
    #         col = i // 10
    #         step_entry.grid(column=col+start_x_cell, row=row+start_y_cell)
    #         dir_entry.grid(column=col+1+start_x_cell, row=row+start_y_cell, columnspan=8)
