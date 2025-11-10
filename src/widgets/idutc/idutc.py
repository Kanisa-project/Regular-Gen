import random
from tkinter import StringVar, OptionMenu, END

from src.widgets import basik_widget

from . import artributalcanvas
from ...settings import themery as t, app_settings


class IDUTC(basik_widget.BasikWidget):
    def __init__(self, width, height, master=None):
        """
        This is the frame for inputting the ID and UTC.

        :param master: Toolbox frame that contains each Tul.
        """
        super().__init__(master=master, width=width, height=height)
        self.configure(text="IDUTC:  ")
        self.setup_text_boxes({"use_id": "r4nd0m",
                               "use_utc": "2134506798"}, start_x_cell=2)
        self.slider_choice_list = ["Transparency", "Coloration", "Animation Speed", "Size", "Motion Range", "Accuracy"]
        self.slider_limit_dict = {"Transparency": [0, 100],
                                  "Coloration": [0, 100],
                                  "Animation Speed": [0, 100],
                                  "Size": [0, 100],
                                  "Motion Range": [0, 100],
                                  "Accuracy": [0, 100]}
        self.setup_slider_bars(self.slider_choice_list, slide_len=width*0.25)

        self.entry_ID_string_var = self.textbox_dict['use_id'][0]
        self.entry_UTC_string_var = self.textbox_dict['use_utc'][0]
        self.id_entry = self.textbox_dict['use_id'][1]
        self.utc_entry = self.textbox_dict['use_utc'][1]
        self.id_entry.config(bg='light yellow')
        self.utc_entry.config(bg='pink')

        # INITIATE THE BUTTONS TO CONTROL USE_ID AND USE_UTC
        self.setup_button_choices(["New ID/UTC", "Set ID/UTC"], start_y_cell=7)
        self.button_dict["New ID/UTC"][1].config(command=self.generate_new_idutc)
        self.button_dict["Set ID/UTC"][1].config(command=self.set_use_idutc)

        self.helper_commands = {
            "set_arty": [self.set_artribute, "Set an artribute for IDUTC.",
                         {}, "IDUT", t.rgb_to_hex(t.LIGHT_CORAL), t.rgb_to_hex(t.DARK_SLATE_GREY)],
            "rando_artries": [self.randomize_artributes, "Randomize the artributes in IDUTC.",
                                  {}, "IDUT", t.rgb_to_hex(t.LIGHT_CORAL), t.rgb_to_hex(t.DARK_SLATE_GREY)],
        }

        self.artyle_artributes_dict = {
            "Data_Source": ["Random", "Human", "Reddit", "OSRS", "Twitter", "Discord"],
            "Transparency": ["Door", "Window"],
            "Coloration": ["Rainbow", "Cloud"],
            "Animation Speed": ["Ice", "Fire"],
            "Size": ["Chicken", "Camel"],
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
            self.artributeMenus[key] = [attribute_str_var,
                                        OptionMenu(self, attribute_str_var, *value)]
            # self.artributeMenus[key][1].grid(column=0, row=2 + list(self.artyle_artributes_dict.keys()).index(key))

        self.kre8dict = self.setup_kre8dict(self.entry_ID_string_var.get(),
                                            self.entry_UTC_string_var.get())
        self.artributal = artributalcanvas.ArtributalCanvas(master=self, width=width * 0.4, height=width * 0.4)
        self.artributal.place(x=width//2, y=height//5)

        self.generate_new_idutc()
        self.artributal.sync_with_use_id()

    def set_artribute(self, new_artribute: str):
        print(new_artribute)
        for artri in list(self.artyle_artributes_dict.keys()):
            if new_artribute.title() in self.artyle_artributes_dict[artri]:
                print("Settingarty: ", artri, new_artribute.title())
                self.kre8dict['artributes'][list(self.artyle_artributes_dict.keys()).index(artri)] = new_artribute.title()
                self.artributal.sync_with_use_id()
                break

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
        self.set_use_idutc()
        self.artributal.sync_with_use_id()

    def set_use_idutc(self):
        """
        Sets up the initial "use_data_dict" to generate the final Meta dictionary.
        :return:
        """
        self.kre8dict = self.setup_kre8dict(self.entry_ID_string_var.get(),
                                            self.entry_UTC_string_var.get())
        self.artributal.sync_with_use_id()

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
    use_id = generate_id_string(6, app_settings.ALPHANUMERIC)
    use_utc = random.randint(app_settings.MIN_CREATION_UTC, app_settings.MAX_CREATION_UTC)
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
        if c.lower() in t.ALPHANUMERIC_COLORS:
            color = t.ALPHANUMERIC_COLORS[c.lower()]
        else:
            color = t.PUNCTUATION_COLORS[c.lower()]
        if is_float:
            color = (round(color[0] / 255, 3),
                     round(color[1] / 255, 3),
                     round(color[2] / 255, 3))

        color_list.append(color)
    return color_list
