import wordieTab
from PIL import Image, ImageDraw, ImageFont
import os
import settings as s


class Collage(wordieTab.Wordietab):
    def __init__(self, master=None):
        super().__init__(master=master)
        collage_areas = ["Border", "Top", "Bottom", "Left", "Right"]
        self.collage_area_dict = init_collage_areas(collage_areas)
        self.setup_text_boxes(self.collage_area_dict, start_x_cell=1, width=42)
        for area in collage_areas:
            self.textbox_dict[area][0].set(s.random_loading_phrase())


def init_collage_areas(areas) -> dict:
    area_dict = {}
    for area in areas:
        area_dict[area] = []
    return area_dict
