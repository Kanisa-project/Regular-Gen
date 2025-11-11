import random
from typing import List

from PIL import Image

from src.widgets.basik_widget import BasikWidget
from src.settings import themery as t
from src.services import utils as u
from src.widgets.glythph import glyther


class Glythph(BasikWidget):
    def __init__(self, width, height, master=None):
        BasikWidget.__init__(self, width=width, height=height, master=master)
        self.setup_button_choices(["All", "None", "Random"])
        self.button_dict["All"][1].configure(command=self.select_all)
        self.button_dict["None"][1].configure(command=self.select_none)
        self.button_dict["Random"][1].configure(command=self.select_random)
        self.setup_radiobutton_choices(['Glyth', 'Glyph'], start_y_cell=3)
        self.checkbutton_choice_list = ["Dirt", "Smoke", "Ripples", "Lightning", "Pebbles",
                                        "Confetti", "Waves", "Fog", "Ash", "Frost",
                                        "Square", "Round", "SlantUp", "SlantDown", "SlantLeft",
                                        "SlantRight", "Ring", "Vertical", "Horizontal", "Up"]
        self.setup_checkbutton_choices(self.checkbutton_choice_list, start_x_cell=2)
        self.helper_commands['gly'] = [self.create_gly, "Creates a glyth/glyph.", {},
                                       "GLYH", u.rgb_to_hex(t.WHITE), u.rgb_to_hex(t.BLACK)]

    def create_gly(self):
        self.txo.priont_list(self.collect_options(), parent_key=['Glyth', 'Glyph'][self.radiobutton_dict['Glyth'][0].get()])
        nim = Image.new("RGBA", (128, 128), u.rgb_to_hex(t.WHITE))
        self.add_glyth(nim, )

    def collect_options(self) -> list:
        chosen_options = []
        for option in self.checkbutton_choice_list:
            if self.checkbutton_dict[option][0].get() == 1:
                chosen_options.append(option)
        return chosen_options

    def select_all(self):
        for option in self.checkbutton_choice_list:
            if self.checkbutton_dict[option][0].get() != 1:
                self.checkbutton_dict[option][0].set(1)

    def select_none(self):
        for option in self.checkbutton_choice_list:
            if self.checkbutton_dict[option][0].get() == 1:
                self.checkbutton_dict[option][0].set(0)

    def select_random(self):
        for option in self.checkbutton_choice_list:
            self.checkbutton_dict[option][0].set(random.randint(0, 1))

    def generate_glyth(self, img: Image.Image, artributes: List[str]):
        pass

    def add_glyth(self, img: Image.Image, kre8dict: dict, abt="masterpiece") -> Image.Image:
        """
        Add each chosen glyth option to the img using the kre8dict.
        """
        artributes = self.set_artributes(kre8dict)
        for glyth_option in kre8dict["glyth"]:
            if glyth_option == "Shadow":
                glyther.shadow(img, artributes)
            if glyth_option == "Dirt":
                glyther.dirt(img, artributes)
            if glyth_option == "Smoke":
                glyther.smoke(img, artributes)
            if glyth_option == "Lightning":
                glyther.lightning(img, artributes)
            if glyth_option == "Pebbles":
                glyther.pebbles(img, artributes)
            if glyth_option == "Confetti":
                glyther.confetti(img, artributes)
            if glyth_option == "Ripples":
                glyther.ripples(img, artributes)
            if glyth_option == "Waves":
                glyther.waves(img, artributes)
            if glyth_option == "Fog":
                glyther.fog(img, artributes)
            if glyth_option == "Frost":
                glyther.frost(img, artributes)
            if glyth_option == "Mist":
                glyther.mist(img, artributes)
            if glyth_option == "Hail":
                glyther.hail(img, artributes)
            if glyth_option == "Embers":
                glyther.embers(img, artributes)
            if glyth_option == "Dust":
                glyther.dust(img, artributes)
            if glyth_option == "Ash":
                glyther.ash(img, artributes)
            if glyth_option == "Flame":
                glyther.flame(img, artributes)
            if glyth_option == "Steam":
                glyther.steam(img, artributes)
        if self.radiobutton_dict["Justin"][0].get() == 1:
            glyther.susan_filter(img, kre8dict)
        if self.radiobutton_dict["Justin"][0].get() == 2:
            glyther.jacob_filter(img, kre8dict)

        return img
