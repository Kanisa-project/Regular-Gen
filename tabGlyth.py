import random
from tkinter import *
from PIL import ImageTk, Image, ImageDraw

import mujic
from settings import *
import artstyle
# from memory_profiler import profile
import glyther


class Glyther(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        """
        A tab that has options to draw basic shapes, lines and dots on the Kinvow.

        :param master: aRtay frame, housing all the other artyles.
        :param idutc: aRtay frame, housing all the other artyles.
        """
        super(Glyther, self).__init__(master=master, width=width, height=height, idutc=idutc)
        self.tkimg = None
        self.tab_name = "Glyth"
        self.checkbutton_choice_list = ["Dirt", "Smoke", "Ripples", "Lightning", "Pebbles",
                                        "Waves", "Fog", "Ash", "Frost", "Mist", "Hail", "Embers", "Dust", "Shadow",
                                        "Glare", "Puddles", "Crystals", "Mud", "Dew", "Steam"]
        # self.air_checkbutton_list = ['Cloud', 'Smoke', 'Wind']
        # self.water_checkbutton_list = ['Wave', 'Ripples', 'Rain']
        # self.earth_checkbutton_list = ['Cloud', 'Smoke', 'Wind']
        # self.fire_checkbutton_list = ['Lightning', 'Ripples', 'Rain']
        self.radiobutton_choice_list = ["None", "Justin", "Susan", "Bethany", "Jacob"]
        self.setup_radiobutton_choices(self.radiobutton_choice_list)
        self.setup_checkbutton_choices(self.checkbutton_choice_list)

    # def load_glyth_options(self, options_to_load: list):
    #     for option in options_to_load:
    #         self.checkbutton_dict[option][0].set(1)

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

    def set_artributes(self, kre8dict: dict) -> list:
        selected_colors = []
        if kre8dict["artributes"][5] == "Pen":
            pass
            # kre8dict["Glyth"]["width"] = kre8dict["number_list"][:3]
        elif kre8dict["artributes"][5] == "Crayon":
            pass
            # kre8dict["Glyth"]["width"] = kre8dict["number_list"][3:]
        if kre8dict["artributes"][1] == "Rainbow":
            for ltr in kre8dict["use_id"]:
                if ltr.lower() in ALPHANUMERIC_COLORS:
                    selected_colors.append(ALPHANUMERIC_COLORS[ltr.lower()])
                else:
                    selected_colors.append(PUNCTUATION_COLORS[ltr.lower()])
        elif kre8dict["artributes"][1] == "Cloud":
            shadelvl = 255 // len(kre8dict["use_id"])
            for i in range(len(kre8dict["use_id"])):
                selected_colors.append(((i + 1) * shadelvl, (i + 1) * shadelvl, (i + 1) * shadelvl))
        return selected_colors

    def add_glyth(self, img: Image, kre8dict: dict, abt="masterpiece") -> Image:
        """
        Add each chosen glyth option to the img using the kre8dict.
        """
        # selected_colors = self.set_artributes(kre8dict)
        for glyth_option in kre8dict["glyth"]:
            if glyth_option == "Shadow":
                glyther.shadow(img, kre8dict)
            if glyth_option == "Dirt":
                glyther.dirt(img, kre8dict)
            if glyth_option == "Smoke":
                glyther.smoke(img, kre8dict)
            if glyth_option == "Lightning":
                glyther.lightning(img, kre8dict)
            if glyth_option == "Pebbles":
                glyther.pebbles(img, kre8dict)
            # if glyth_option == "Confetti":
            #     glyther.confetti(img, kre8dict)
            if glyth_option == "Ripples":
                glyther.ripples(img, kre8dict)
            if glyth_option == "Waves":
                glyther.waves(img, kre8dict)
            if glyth_option == "Fog":
                glyther.fog(img, kre8dict)
            if glyth_option == "Frost":
                glyther.frost(img, kre8dict)
            if glyth_option == "Mist":
                glyther.mist(img, kre8dict)
            if glyth_option == "Hail":
                glyther.hail(img, kre8dict)
            if glyth_option == "Embers":
                glyther.embers(img, kre8dict)
            if glyth_option == "Dust":
                glyther.dust(img, kre8dict)
            if glyth_option == "Ash":
                glyther.ash(img, kre8dict)
        if self.radiobutton_dict["Justin"][0].get() == 1:
            glyther.susan_filter(img, kre8dict)
        if self.radiobutton_dict["Justin"][0].get() == 2:
            glyther.jacob_filter(img, kre8dict)

        return img
