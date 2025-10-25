import random

from PIL import Image

from . import artstyle
from ...features.artay import glyther


class Glyther(artstyle.Artyle):
    def __init__(self, width, height, master=None):
        """
        A tab that has options to draw basic shapes, lines and dots on the Kinvow.

        :param master: aRtay frame, housing all the other artay.
        :param idutc: aRtay frame, housing all the other artay.
        """
        super(Glyther, self).__init__(master=master, width=width, height=height)
        self.tkimg = None
        self.tab_name = "Glyth"
        self.checkbutton_choice_list = ["Dirt", "Smoke", "Ripples", "Lightning", "Pebbles", "Confetti",
                                        "Waves", "Fog", "Ash", "Frost", "Mist", "Hail", "Embers", "Dust", "Shadow",
                                        "Glare", "Puddles", "Crystals", "Mud", "Dew", "Steam", "Flame"]
        self.radiobutton_choice_list = ["None", "Justin", "Susan", "Bethany", "Jacob"]
        self.selection_button_list = ["All", "None", "Random"]
        self.setup_button_choices(self.selection_button_list)
        self.button_dict["All"][1].configure(command=self.select_all)
        self.button_dict["None"][1].configure(command=self.select_none)
        self.button_dict["Random"][1].configure(command=self.select_random)
        self.setup_radiobutton_choices(self.radiobutton_choice_list, start_y_cell=3)
        self.setup_checkbutton_choices(self.checkbutton_choice_list, start_x_cell=2)

    def gather_glyth_options(self) -> list:
        """Gather and return the options Glyther will use to draw."""
        chosen_glyth_options = []
        for option in self.checkbutton_choice_list:
            if self.checkbutton_dict[option][0].get() == 1:
                chosen_glyth_options.append(option)
        return chosen_glyth_options

    def gather_random_options(self) -> list:
        """Gather and return the options Glyther will use to draw."""
        chosen_glyth_options = []
        for option in self.checkbutton_choice_list:
            self.checkbutton_dict[option][0] = random.randint(0, 1)
            if self.checkbutton_dict[option][0] == 1:
                chosen_glyth_options.append(option)
        return chosen_glyth_options

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

    def command_glyth_options(self, command_arg) -> list:
        chosen_glyth_options = []
        if isinstance(command_arg, str):
            for i in range(int(command_arg)):
                option = random.choice(self.checkbutton_choice_list)
                chosen_glyth_options.append(option)
        return chosen_glyth_options
