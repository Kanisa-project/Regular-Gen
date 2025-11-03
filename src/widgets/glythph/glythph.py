import random

from src.widgets.basik_widget import BasikWidget
from src.settings import themery as t, utils as u
from src.widgets.glythph import glyther
from src.widgets.glythph import glyphinator

class Glythph(BasikWidget):
    def __init__(self, width, height, master=None):
        super().__init__(width, height, master)

        self.setup_button_choices(["All", "None", "Random"])

        self.button_dict["All"][1].configure(command=self.select_all)
        self.button_dict["None"][1].configure(command=self.select_none)
        self.button_dict["Random"][1].configure(command=self.select_random)
        self.setup_radiobutton_choices(['Glyth', 'Glyph'], start_x_cell=1)
        self.checkbutton_choice_list = ["Dirt", "Smoke", "Ripples", "Lightning", "Pebbles",
                                        "Confetti", "Waves", "Fog", "Ash", "Frost",
                                        "Square", "Round", "SlantUp", "SlantDown", "SlantLeft",
                                        "SlantRight", "Ring", "Vertical", "Horizontal", "Up"]
        self.setup_checkbutton_choices(self.checkbutton_choice_list, start_x_cell=2)
        self.helper_commands['gly'] = [self.create_gly, "Creates a glyth/glyph.", {},
                                       "GLYH", u.rgb_to_hex(t.WHITE), u.rgb_to_hex(t.BLACK)]

    def create_gly(self):
        self.txo.priont_list(self.collect_options())

    def collect_options(self) -> list:
        chosen_options = []
        print(self.radiobutton_dict)
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
