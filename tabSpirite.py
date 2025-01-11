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
        self.tab_name = "spirite"
        self.spirite_optionmenu_choice_list = ["None", "Alien", "Asteroid", "Ball", "Medallion", "Ship", "Sword",
                                               "Tribloc", "RTJ", "Boat", "Platform", "Goal"]
        self.setup_dropdown_menus(word_list=self.spirite_optionmenu_choice_list, dropdown_name="spirite_type")
        self.spirite_str = self.dropdown_menu_dict["spirite_type"][0].get()
        self.layer_name_dict = LAYER_DICT[self.spirite_str]
        self.chosen_spirite_layer_dict = {}
        self.update_layer_dropdowns(list(self.layer_name_dict.keys()))

    def update_layer_dropdowns(self, new_layer_list: list):
        print("UPDATING", new_layer_list)
        for layer_name, layer_numbers in self.layer_name_dict.items():
            lbl_name = tk.Label(master=self, text=layer_name)
            lbl_name.grid(column=3, row=new_layer_list.index(layer_name))
            layer_nbr_var = IntVar()
            layer_nbr_dropdown = ttk.OptionMenu(self, layer_nbr_var, *list(range(-1, 10)))
            layer_nbr_var.set(0)
            layer_nbr_dropdown.grid(column=4, row=new_layer_list.index(layer_name))

    def setup_dropdown_menus(self, word_list=None, word_str=None, dropdown_name=""):
        super().setup_dropdown_menus(word_list=word_list, word_str=word_str, dropdown_name=dropdown_name)

    def update_spirite_str(self):
        self.spirite_str = self.dropdown_menu_dict["spirite_type"][0].get()

    def gather_spirite_options(self) -> dict:
        """Gather Spirite options into a dictionary."""
        chosen_spirite_type = self.dropdown_menu_dict["spirite_type"][0].get()
        chosen_spirite_options = {
            chosen_spirite_type: LAYER_DICT[chosen_spirite_type]
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

    def setup_wordlist_optionmenus(self, word_str: str):
        """Create optionmenus for each wordlist."""
        super().setup_dropdown_menus(word_str)

    def setup_layer_optionmenus(self, list_of_layers: list):
        super().setup_dropdown_menus(word_list=list_of_layers)

    def add_spirite(self, img: Image, kre8dict: dict, abt='masterpiece') -> Image:
        """
        Add a spirite to the masterpiece.
        :param abt:
        :param img:
        :param kre8dict:
        :return:
        """
        w, h = img.size
        spirite_layers = []
        sw, sh = (128, 128)
        fraim = spirite.stack_layers(img, kre8dict, (sw, sh))
        spirite_layers.append(fraim)
        for layer in spirite_layers:
            img.paste(layer, ((w // 2) - sw // 2, (h // 2) - sh // 2), mask=layer)
        return img
