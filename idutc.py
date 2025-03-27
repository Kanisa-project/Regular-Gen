# import datetime
import json
import os.path
import random
# import tkinter as tk
from dataclasses import dataclass
from tkinter import *
from tkinter.filedialog import askopenfilename

import artributal_canvas
import helper_widget
import settings as s
import mtgsdk as mtg


@dataclass
class kre8dict:
    number_list: list
    color_list: list
    artributes: list
    masterpiece: dict


class IDUTC(helper_widget.helpingWidget):
    def __init__(self, width, height, master=None):
        """
        This is the frame for inputting the ID and UTC.

        :param master: Toolbox frame that contains each Tul.
        """
        super().__init__(master=master, width=width, height=height)
        self.configure(text="IDUTC:  ")
        self.grid_propagate(False)
        self.setup_text_boxes({"use_id": "r4nd0m",
                               "use_utc": "2134506798"}, width=16)
        self.slider_choice_list = ["Transparency", "Coloration", "Animation Speed", "Size", "Motion Range", "Accuracy"]
        self.slider_limit_dict = {"Transparency": [0, 100],
                                  "Coloration": [0, 100],
                                  "Animation Speed": [0, 100],
                                  "Size": [0, 100],
                                  "Motion Range": [0, 100],
                                  "Accuracy": [0, 100]}
        self.setup_slider_bars(self.slider_choice_list, start_x_cell=2, start_y_cell=3, slide_len=175)

        self.entry_ID_string_var = self.textbox_dict['use_id'][0]
        self.entry_UTC_string_var = self.textbox_dict['use_utc'][0]
        self.id_entry = self.textbox_dict['use_id'][1]
        self.utc_entry = self.textbox_dict['use_utc'][1]
        self.id_entry.config(bg='light yellow')
        self.utc_entry.config(bg='pink')

        # INITIATE THE BUTTONS TO CONTROL USE_ID AND USE_UTC
        self.setup_button_choices(["New ID/UTC", "Set ID/UTC"], start_x_cell=4)
        self.setup_button_choices(["Save kre8dict", "Load kre8dict"], start_x_cell=5)
        self.button_dict["New ID/UTC"][1].config(command=self.generate_new_idutc)
        self.button_dict["Set ID/UTC"][1].config(command=self.set_use_idutc)
        self.button_dict["Save kre8dict"][1].config(command=self.save_json)
        self.button_dict["Load kre8dict"][1].config(command=self.load_json)
        self.texioty_commands = {
            "random_artributes": [self.randomize_artributes, "Randomize the artributes in IDUTC.",
                                  {}, "IDUT", s.rgb_to_hex(s.LIGHT_CORAL), s.rgb_to_hex(s.DARK_SLATE_GREY)],
        }

        self.artyle_artributes_dict = {
            "Data_Source": ["Random", "Human", "Reddit", "OSRS", "Twitter", "Discord"],
            "Transparency": ["Door", "Window"],
            "Coloration": ["Rainbow", "Cloud"],
            "Animation Speed": ["Ice", "Fire"],
            "Size": ["Chicken", "Dog", "Camel"],
            "Motion Range": ["Sock", "Rock"],
            "Accuracy": ["Pen", "Crayon"]
        }
        self.artributeMenus = {}
        for key, value in self.artyle_artributes_dict.items():
            attribute_str_var = StringVar()
            attribute_str_var.set(random.choice(value))
            if key == "Data_Source":
                # ~~ set data_source to what you want
                attribute_str_var.set("Random")
            elif key == "Size":
                # ~~ set size to what you want
                attribute_str_var.set("Dog")
            self.artributeMenus[key] = [attribute_str_var,
                                        OptionMenu(self, attribute_str_var, *value)]
            self.artributeMenus[key][1].grid(column=0, row=2 + list(self.artyle_artributes_dict.keys()).index(key))

        # self.generate_new_idutc()
        self.entry_ID_string_var.set("r4nd0m")
        self.entry_UTC_string_var.set("0000000000")
        # self.set_use_idutc()
        # self.kre8dict = self.setup_kre8dict(self.textbox_dict['use_id'][0].get(),
        #                                     self.textbox_dict['use_utc'][0].get())
        self.kre8dict = self.setup_kre8dict(self.entry_ID_string_var.get(),
                                            self.entry_UTC_string_var.get())
        self.artributal = artributal_canvas.artributalCanvas(master=self, width=width * 0.375, height=width * 0.375)
        # self.artributeMenus = self.artributal.artributeMenus
        if not self.search_and_load_origin():
            # self.txo.fresh_start_no_profile()
            print("NNNNNOPPPE", width)

    def create_blank_profile(self):
        pass

    def gather_attributes(self) -> list:
        """Gather and return a list of attribute keywords."""
        attribs_list = []
        # print("GATHERING", self.artributeMenus)
        for key, value in self.artributeMenus.items():
            attribs_list.append(value[0].get())
        return attribs_list

    def gather_random_attributes(self) -> list:
        """Gather and return a list of attribute keywords."""
        attribs_list = []
        # print("ARTRIB", self.artyle_artributes_dict)
        for key, value in self.artyle_artributes_dict.items():
            attribs_list.append(random.choice(value))
        return attribs_list

    def generate_new_idutc(self):
        """
        Generate a new random IDUTC
        """
        use_id, use_utc = create_id_utc()
        self.id_entry.delete(0, END)
        self.utc_entry.delete(0, END)
        self.id_entry.insert(0, use_id)
        self.utc_entry.insert(0, str(use_utc))

    def set_use_idutc(self):
        """
        Sets up the initial "use_data_dict" to generate the final Meta dictionary.
        :return:
        """
        self.kre8dict = self.setup_kre8dict(self.entry_ID_string_var.get(),
                                            self.entry_UTC_string_var.get())

    def save_json(self):
        """
        Saves the kre8dict dictionary as a JSON file in the folder of kre8dict use_id.
        :return:
        """
        use_id = self.kre8dict["use_id"]
        use_utc = self.kre8dict["use_utc"]
        dumpDict = self.kre8dict
        print(use_utc, type(use_utc))
        save_dir = self.txo.master.active_profile.username
        if not os.path.exists(use_id) and use_utc == "0000000000":
            os.makedirs(use_id)
            save_dir = use_id
        try:
            with open(f'{save_dir}/{use_id}_{use_utc}.json', 'w') as f:
                json.dump(dumpDict, f, indent=4)
        except FileNotFoundError as e:
            self.txo.priont_string(str(e))
        finally:
            pass

    def save_json_pen(self, pen_dict: dict):
        """
        Saves a kanisaPen file
        :return:
        """
        dumpDict = pen_dict
        with open(f'kanisaPens/{pen_dict["use_id"]}_{pen_dict["use_utc"]}.json', 'w') as f:
            json.dump(dumpDict, f, indent=4)

    def load_json(self):
        """Loads an idutc from a json file."""
        home_path = '/home/trevor/PythonProjects/kanisaWallet'
        loaded_file = askopenfilename(initialdir=f'{home_path}/{self.entry_ID_string_var.get()}')
        with open(loaded_file, 'r') as file:
            try:
                loaded_data = json.load(file)
            finally:
                pass
        self.entry_ID_string_var.set(loaded_data['use_id'])
        self.entry_UTC_string_var.set(loaded_data['use_utc'])
        self.kre8dict = loaded_data
        # for artyle, chosen_options in self.kre8dict.items():
        #     print(artyle, chosen_options)

    def load_pen(self):
        """Loads an kanisaPen from a json file."""
        home_path = '/home/trevor/PythonProjects/kanisaWallet/kanisaPens'
        loaded_file = askopenfilename(initialdir=f'{home_path}/{self.entry_ID_string_var.get()}')
        with open(loaded_file, 'r') as file:
            try:
                loaded_data = json.load(file)
            finally:
                pass
        self.entry_ID_string_var.set(loaded_data['use_id'])
        self.entry_UTC_string_var.set(loaded_data['use_utc'])
        self.kre8dict = loaded_data
        for artyle, chosen_options in self.kre8dict.items():
            print(artyle, chosen_options)

    def setup_kre8dict(self, use_id: str, use_utc: str) -> dict:
        """
        Sets up the initial KRE8shun dictionary.
        """
        number_list = new_number_list(use_utc)
        number_list.sort()
        creation_dict = {
            "use_id": use_id,
            "use_utc": use_utc,
            "color_list": new_color_list(use_id, is_float=False),
            "number_list": number_list,
            "artributes": self.gather_attributes()
        }
        return creation_dict

    def randomize_artributes(self, args):
        for key, value in self.artyle_artributes_dict.items():
            self.artributeMenus[key][0].set(random.choice(value))

    def search_and_load_origin(self):
        for item in os.listdir(os.getcwd()):
            if os.path.isdir(item):
                if os.path.exists(f'{item}/0000000000.json'):
                    print("Founded origin in ", item)
                    with open(f'{os.getcwd()}/{item}/0000000000.json', 'r') as file:
                        print("Opened:", f'{os.getcwd()}/{item}/0000000000.json')
                        try:
                            loaded_data = json.load(file)
                            print("Loaded:", loaded_data)
                        finally:
                            pass
                    self.textbox_dict['use_id'][0].set(loaded_data['use_id'])
                    self.textbox_dict['use_utc'][0].set(loaded_data['use_utc'])
                    self.kre8dict = loaded_data
                else:
                    return False


def construct_file_path(base_path, attributes, filename):
    return f"{base_path}/{attributes[3]}/{filename}.png"


def add_data_source_dict(use_data: dict):
    """
    Adds data_source dictionary keys and values for the data source info.
    :param use_data: dictionary to add data source infor to.
    :return:
    """
    if use_data["data_source"] == "Reddit":
        # submission = reddit.submission(use_data["use_ID"])
        use_data["link"] = f'https://www.reddit.com/{use_data["use_ID"]}'
        # use_data["submission"] = submission
    elif use_data["data_source"] == "OSRS":
        use_data["OSRS Player"] = "OSRSSTUFF"
        use_data["Player Skills"] = ["Attack", "Defence", "Prayer"]
    elif use_data["data_source"] == "MTG":
        # card_name = use_data["use_id"]
        named_cards = mtg.Card.where(name="Boros").all()
        if len(named_cards) == 0:
            named_cards = mtg.Card.where(name="King").all()
        chosen_card = random.choice(named_cards)
        flavor_list = []
        lz = '0'
        if len(str(chosen_card.multiverse_id)) < 10:
            lz *= 10 - len(str(chosen_card.multiverse_id))
        for card in named_cards:
            if card.flavor not in flavor_list:
                flavor_list.append(card.flavor)

    elif use_data["data_source"] == "Human":
        # use_data["name"] = ""
        pass
    elif use_data["data_source"] == "Barcode":
        use_data["item_name"] = ""
        use_data["item_info"] = []


def create_button(parent, text, command, width, column, row):
    new_button = Button(parent, text=text, command=command, width=width)
    new_button.grid(column=column, row=row)
    return new_button


def create_attribute_menu(parent, attribute_var, attribute_options, column, row):
    menu = OptionMenu(parent, attribute_var, *attribute_options)
    menu.grid(column=column, row=row)
    return menu


def generate_id_string(string_length, char_set) -> str:
    """
    Generate an ID string given the string_length of ID and the character set to use.

    :param string_length: The length the ID string will be.
    :param char_set: A string of characters to choose from.
    :return: ID string for use.
    """
    ID_string = ""
    for i in range(string_length):
        ID_string += char_set[random.randint(0, len(char_set) - 1)]
    return ID_string


def create_id_utc() -> (str, str):
    """
    Creates a new idutc based on data_source variable.
    :return: Tuple of strings, an ID and UTC
    """
    use_id = generate_id_string(6, s.ALPHANUMERIC)
    use_utc = random.randint(s.MIN_CREATION_UTC, s.MAX_CREATION_UTC)
    return use_id, use_utc


def new_number_list(utc_used: str) -> list:
    """
    Make a list of numbers from the 10-digit number string and return sorted list.
    """
    number_list = []
    for i in range(10):
        # print(i)
        xs = list(utc_used)[i]
        number_list.append(int(xs))
    number_list.sort()
    return number_list


def new_color_list(id_used: str, is_float=True) -> list:
    """
    Create a new color list with the given ID string.

    :param id_used: ID string being used to create the color list.
    :param is_float: If the tuple is created with Floats or Integers.
    :return: list
    """
    color_list = []
    for c in id_used:
        if c.lower() in s.ALPHANUMERIC_COLORS:
            color = s.ALPHANUMERIC_COLORS[c.lower()]
        else:
            color = s.PUNCTUATION_COLORS[c.lower()]
        if is_float:
            color = (round(color[0] / 255, 3),
                     round(color[1] / 255, 3),
                     round(color[2] / 255, 3))

        color_list.append(color)
    return color_list
