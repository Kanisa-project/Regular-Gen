import random

import wordieTab
from PIL import Image, ImageDraw, ImageFont
import os
import settings as s


class Collage(wordieTab.Wordietab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.collage_areas = ["Border", "Top", "Bottom", "Left", "Right"]
        self.collage_area_dict = init_collage_areas(self.collage_areas)
        self.setup_text_boxes(self.collage_area_dict, start_x_cell=1, width=42)
        self.setup_button_choices(["RandoCapSpaced"])
        self.button_dict["RandoCapSpaced"][1].config(command=self.shuffle_case_the_areas)
        for area in self.collage_areas:
            self.textbox_dict[area][0].set(s.random_loading_phrase())

    def shuffle_case_the_areas(self):
        for area in self.collage_areas:
            self.textbox_dict[area][0].set(random_capitalization_space_between(self.master.master.idutc_frame.kre8dict['use_id']))


def init_collage_areas(areas) -> dict:
    area_dict = {}
    for area in areas:
        area_dict[area] = []
    return area_dict


def random_capitalization_space_between(word: str) -> str:
    gamestopped_word = ""
    for letter in word:
        if random.random() >= 0.5:
            letter = letter.upper()
        gamestopped_word += letter + " "
    return gamestopped_word
