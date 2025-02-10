import random
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageDraw, ImageTk

import artstyle
import glyphinator
from settings import *


class Glyphin(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        """
        A tab with options for loading images and placing them on the Kinvow in a grid style of pattern.

        :param master: aRtay frame, housing all the artyles.
        """
        super(Glyphin, self).__init__(master=master, idutc=idutc, width=width, height=height)
        self.tab_name = "Glyph"
        # self.radiobutton_choice_list = ["masterpiece", "Avatar", "Banner", "Tile"]
        self.checkbutton_choice_list = ["Square", "Round", "SlantUp", "SlantDown", "SlantLeft", "SlantRight", "Ring",
                                        "Vertical", "Horizontal", "Up", "Down", "Left", "Right", "Snow", "Scales",
                                        "Plaid"]
        self.selection_button_list = ["All", "None", "Random"]
        # self.tone_int_var = IntVar()
        # self.disp_img = None
        # self.setup_radiobutton_choices(self.radiobutton_choice_list)
        self.setup_button_choices(self.selection_button_list)
        self.setup_checkbutton_choices(self.checkbutton_choice_list)
        self.button_dict["All"][1].configure(command=self.select_all)
        self.button_dict["None"][1].configure(command=self.select_none)
        self.button_dict["Random"][1].configure(command=self.select_random)

    def gather_glyph_options(self) -> list:
        """Gather the options from this tab and return them as a dictionary."""
        chosen_glyph_options = []
        for option in self.checkbutton_choice_list:
            if self.checkbutton_dict[option][0].get() == 1:
                chosen_glyph_options.append(option)
        return chosen_glyph_options

    def gather_random_options(self) -> list:
        """Gather the options from this tab and return them as a dictionary."""
        chosen_glyph_options = []
        for option in self.checkbutton_choice_list:
            self.checkbutton_dict[option][0] = random.randint(0, 1)
            if self.checkbutton_dict[option][0] == 1:
                chosen_glyph_options.append(option)
        return chosen_glyph_options

    def add_glyph(self, img: Image, kre8dict: dict, abt="masterpiece") -> Image:
        """
        Bring in an image, add some kre8dict things to it about whatever it is. Get new image back.
        :param img:
        :param kre8dict:
        :param abt:
        :return:
        """
        w, h = img.size
        # bity = Image.new("RGBA", (64, 64), DRS_PURPLE)
        selected_colors = []
        # print(kre8dict)
        if kre8dict["artributes"][2] == "Rainbow":
            for ltr in kre8dict["use_id"]:
                selected_colors.append(ALPHANUMERIC_COLORS[ltr])
        elif kre8dict["artributes"][2] == "Cloud":
            shadelvl = 255 // len(kre8dict["use_id"])
            for i in range(len(kre8dict["use_id"])):
                selected_colors.append(((i + 1) * shadelvl, (i + 1) * shadelvl, (i + 1) * shadelvl))
        for x in range(0, w, 64):
            for y in range(0, h, 64):
                # if len(kre8dict) == 0:
                #     kre8dict.append("Emoji")
                bit_type = random.choice(kre8dict["glyph"])
                bity = Image.new("RGBA", (64, 64), DRS_PURPLE)
                if bit_type == "Vertical":
                    bity = glyphinator.vertical_bity(bity, selected_colors)
                if bit_type == "Horizontal":
                    bity = glyphinator.horizontal_bity(bity, selected_colors)
                if bit_type == "SlantUp":
                    bity = glyphinator.slant_up_bity(bity, selected_colors)
                if bit_type == "SlantDown":
                    bity = glyphinator.slant_down_bity(bity, selected_colors)
                if bit_type == "SlantLeft":
                    bity = glyphinator.slant_left_bity(bity, selected_colors)
                if bit_type == "SlantRight":
                    bity = glyphinator.slant_right_bity(bity, selected_colors)
                if bit_type == "Up":
                    bity = glyphinator.up_bity(bity, selected_colors)
                if bit_type == "Down":
                    bity = glyphinator.down_bity(bity, selected_colors)
                if bit_type == "Left":
                    bity = glyphinator.left_bity(bity, selected_colors)
                if bit_type == "Right":
                    bity = glyphinator.right_bity(bity, selected_colors)
                if bit_type == "Square":
                    bity = glyphinator.square_bity(bity, selected_colors)
                if bit_type == "Round":
                    bity = glyphinator.round_bity(bity, selected_colors)
                if bit_type == "Ring":
                    bity = glyphinator.ring_bity(bity, selected_colors)
                if bit_type == "Snow":
                    bity = glyphinator.snow_bity(bity, selected_colors)
                if bit_type == "Plaid":
                    bity = glyphinator.plaid_bity(bity, selected_colors)
                if bit_type == "Emoji":
                    bity = glyphinator.emoji_bity(bity, selected_colors)
                if bit_type == "Scales":
                    bity = glyphinator.scales_bity(bity, selected_colors)
                # print(bity, bit_type)
                img.paste(bity, (x, y))
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
