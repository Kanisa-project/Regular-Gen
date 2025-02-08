from tkinter import *
from PIL import ImageDraw
import artstyle
import numpy as np
import wavio as wavio
import mujic
from settings import *


class Mujic(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        """
        Musical masterpiece with a pinch of magic.
        :param master:
        :param idutc:
        """
        super(Mujic, self).__init__(master=master, idutc=idutc, width=width, height=height)
        self.tab_name = "Mujic"
        self.slider_choice_list = ["Note duration", "Base frequency"]
        self.setup_radiobutton_choices(["Sine", "Sweep", "Chirp", "Convolve", "Mixture"])
        self.slider_limit_dict = {
            "Note duration": [2, 32],
            "Base frequency": [40, 80],
            }
        self.setup_dropdown_menus(word_str="1234")
        self.setup_slider_bars(self.slider_choice_list)
        self.slider_dict["Note duration"][3].grid(column=5, row=0)
        self.slider_dict["Note duration"][2].grid(column=6, row=0)
        self.slider_dict["Base frequency"][3].grid(column=5, row=1)
        self.slider_dict["Base frequency"][2].grid(column=6, row=1)
        self.note_pattern_str_var = StringVar()
        self.note_pattern_label = Label(self, textvariable=self.note_pattern_str_var)
        self.note_pattern_label.grid(column=0, row=4)
        self.note_pattern_int_var = IntVar()
        # self.tone_freq_dict = mujic.generate_tone_notes(0.25)

    def gather_mujic_options(self) -> dict:
        """Gather and return the options Mujic will use to make what it makes."""
        chosen_mujic_options = {}
        dict_key_list = list(self.dropdown_menu_dict.keys())
        chosen_mujic_options["First Pat"] = self.dropdown_menu_dict[dict_key_list[0]][0].get()
        chosen_mujic_options["Second Pat"] = self.dropdown_menu_dict[dict_key_list[1]][0].get()
        chosen_mujic_options["Third Pat"] = self.dropdown_menu_dict[dict_key_list[2]][0].get()
        chosen_mujic_options["Fourth Pat"] = self.dropdown_menu_dict[dict_key_list[3]][0].get()
        chosen_mujic_options["Note duration"] = self.slider_dict["Note duration"][0].get()
        chosen_mujic_options["Base frequency"] = self.slider_dict["Base frequency"][0].get()
        if self.radiobutton_dict["Chirp"][0].get() == 0:
            chosen_mujic_options["Wave type"] = "Sine"
        if self.radiobutton_dict["Chirp"][0].get() == 1:
            chosen_mujic_options["Wave type"] = "Sweep"
        if self.radiobutton_dict["Chirp"][0].get() == 2:
            chosen_mujic_options["Wave type"] = "Chirp"
        if self.radiobutton_dict["Chirp"][0].get() == 3:
            chosen_mujic_options["Wave type"] = "Convolve"
        return chosen_mujic_options

    def destroy_word_optionmenus(self):
        """Destroy each of the optionmenus that contain wordlists"""
        for c in self.optionmenu_dict:
            self.optionmenu_dict[c][1].destroy()

    def add_mujic(self, img: Image, kre8dict: dict, abt='masterpiece') -> Image:
        # mujic.save_the_mujic(kre8dict)
        self.create_mujical_piece(img, kre8dict)
        w, h = img.size
        cx, cy = w//2, h//2
        draw = ImageDraw.Draw(img)
        draw.line((cx, cy, cx, cy+64), fill=BLACK, width=2)
        draw.line((cx+64, cy, cx+64, cy+80), fill=BLACK, width=2)
        draw.line((cx, cy, cx+64, cy), fill=BLACK, width=2)

        draw.ellipse((cx-4, cy+56, cx+16, cy+72), fill=BLACK)
        draw.ellipse((cx+60, cy+56, cx+96, cy+88), fill=BLACK)
        return img

    def create_mujical_piece(self, img: Image, kre8dict: dict) -> Image:
        """
        Create the piece of mujical talent.
        :param img:
        :param kre8dict:
        :return:
        """
        mujic_data = mujic.create_song_data(kre8dict)
        # mujic_data = mujic.get_song_data(kre8dict['use_id'])
        mujic_data = mujic_data * (16300 / np.max(mujic_data))
        mujic_data = mujic_data.astype(np.int16)
        wavio.write(f"{kre8dict['use_id']}/{kre8dict['use_utc']}.wav", mujic_data, 44100)
        return img
