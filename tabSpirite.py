import random
from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import ImageTk

import artstyle
import spirite
from settings import *


class Spirite(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        """
        A tab with options for loading different spirite layers. First select a spirit you would like to turn into a
        sprite, and then select the various different layers or have the computer make a random one.

        :param master: aRtay frame, housing all the other artyles.
        """
        super(Spirite, self).__init__(master=master, idutc=idutc, width=int(width), height=height)
        self.tab_name = "Spirite"
        self.spirite_optionmenu_choice_list = ["None", "Alien", "Asteroid", "Ball", "Medallion", "Ship", "Sword",
                                               "Tribloc", "RTJ", "Boat", "Platform", "Goal"]
        self.setup_dropdown_menus(word_list=self.spirite_optionmenu_choice_list, dropdown_name="spirite_type")
        self.setup_button_choices(['Randomize All'], start_y_cell=1)
        self.button_dict['Randomize All'][1].config(command=self.randomize_all_layer_number)
        self.spirite_str = self.dropdown_menu_dict["spirite_type"][0].get()
        self.layer_name_dict = LAYER_DICT[self.spirite_str]
        self.chosen_spirite_layer_dict = {}
        self.layer_number_wheel_dict = {}
        self.setup_layer_dropdowns(list(self.layer_name_dict.keys()))

    def setup_layer_dropdowns(self, new_layer_list: list):
        for layer_name, layer_numbers in self.layer_name_dict.items():
            lbl_str = StringVar()
            lbl_name = tk.Label(master=self, textvariable=lbl_str)
            lbl_name.grid(column=3, row=new_layer_list.index(layer_name))
            layer_nbr_var = IntVar()
            layer_nbr_dropdown = ttk.OptionMenu(self, layer_nbr_var, *list(range(-1, 10)),
                                                command=self.update_layer_number)
            layer_nbr_var.set(0)
            layer_nbr_dropdown.grid(column=4, row=new_layer_list.index(layer_name))
            layer_nbr_dropdown.bind("<Button-3>", self.randomize_layer_number)
            self.layer_number_wheel_dict[f'layer_{new_layer_list.index(layer_name)}'] = [lbl_str, layer_nbr_var]

    def randomize_layer_number(self, layered):
        self.layer_number_wheel_dict[f'layer_{random.randint(0,3)}'][1].set(random.randint(0, 9))
        pass

    def update_layer_number(self, new_layer_num):
        pass

    def update_layer_dropdowns(self, new_layer_list: list):
        for layer_name, layer_numbers in self.layer_name_dict.items():
            print("UPDATE: ", layer_name, new_layer_list.index(layer_name))
            self.layer_number_wheel_dict[f'layer_{new_layer_list.index(layer_name)}'][0].set(layer_name)

    def setup_dropdown_menus(self, word_list=None, word_str=None, dropdown_name="", start_x_cell=0, start_y_cell=0):
        # If it is a single string, collect random words for the dropdown menu
        if word_str:
            self.widget_display_array.append(word_str)
            for c in word_str:
                while c in self.dropdown_menu_dict:
                    c += c
                words_str_var = StringVar(value=ALPHANUMERIC_WORD_LISTS[c[:1].lower()][0])
                self.dropdown_menu_dict[c] = [words_str_var,
                                              OptionMenu(self, words_str_var, *ALPHANUMERIC_WORD_LISTS[c[:1].lower()])]
        # If it's a list, just add the list of words to the dropdown menu.
        elif word_list:
            self.widget_display_array.append(dropdown_name)
            word_str_var = StringVar(value=word_list[0])
            self.dropdown_menu_dict[dropdown_name] = [word_str_var,
                                                      OptionMenu(self, word_str_var, *word_list,
                                                                 command=self.update_spirite_str)]
        # Add each dropdown menu to the artyle frame.
        for i, dropdown in enumerate(list(self.dropdown_menu_dict.keys())):
            row = i % 10
            col = i // 10
            self.dropdown_menu_dict[dropdown][1].grid(column=start_x_cell+col, row=start_y_cell+row)

    def update_spirite_str(self, morestuff):
        print("MORE", morestuff)
        self.spirite_str = self.dropdown_menu_dict["spirite_type"][0].get()
        self.layer_name_dict = LAYER_DICT[self.spirite_str]
        self.update_layer_dropdowns(list(self.layer_name_dict.keys()))

    def gather_spirite_options(self) -> dict:
        """Gather Spirite options into a dictionary."""
        chosen_spirite_type = self.dropdown_menu_dict["spirite_type"][0].get()
        chosen_spirite_options = {
            chosen_spirite_type: LAYER_DICT[chosen_spirite_type],
            "layer_one_list": self.layer_number_wheel_dict['layer_0'],
            "layer_two_list": self.layer_number_wheel_dict['layer_1'],
            "layer_three_list": self.layer_number_wheel_dict['layer_2'],
            "layer_four_list": self.layer_number_wheel_dict['layer_3']
        }
        return chosen_spirite_options

    def gather_random_options(self) -> dict:
        """Gather Spirite options into a dictionary."""
        random_spirite = random.choice(["Asteroid", "Alien", "Ship", "Medallion"])
        chosen_spirite_type = random_spirite
        chosen_spirite_options = {
            chosen_spirite_type: LAYER_DICT[chosen_spirite_type]
        }
        return chosen_spirite_options

    # def generate_populate_spirite_choices(self):
    #     self.destroy_word_optionmenus()
    #     self.setup_dropdown_menus()
    #
    # def destroy_word_optionmenus(self):
    #     """Destroy each of the optionmenus that contain wordlists"""
    #     for layer_name in self.layer_name_dict:
    #         self.chosen_spirite_layer_dict[layer_name][1].destroy()

    # def setup_wordlist_optionmenus(self, word_str: str):
    #     """Create optionmenus for each wordlist."""
    #     super().setup_dropdown_menus(word_str)

    def setup_layer_optionmenus(self):
        super().setup_dropdown_menus(word_list=list(self.layer_name_dict.keys()))

    def add_spirite(self, img: Image, kre8dict: dict, abt='masterpiece') -> Image:
        """
        Add a spirite to the masterpiece.
        :param abt:
        :param img:
        :param kre8dict:
        :return:
        """
        artribute_dict = self.set_artributes(kre8dict)
        artribute_dict['spirite'] = kre8dict['spirite']
        w, h = img.size
        spirite_layers = []
        sw, sh = (128, 128)
        fraim = spirite.stack_layers(img, artribute_dict, (sw, sh))
        spirite_layers.append(fraim)
        for layer in spirite_layers:
            img.paste(layer, ((w // 2) - sw // 2, (h // 2) - sh // 2), mask=layer)
        return img

    def randomize_all_layer_number(self):
        for lay_num in range(4):
            self.layer_number_wheel_dict[f'layer_{lay_num}'][1].set(random.randint(0, 9))
