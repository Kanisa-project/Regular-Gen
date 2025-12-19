import glob
import json
import os
import re
import shutil
from tkinter import Canvas, Button, OptionMenu, StringVar, PhotoImage
from typing import Optional, List

from src.domain.resource_loader import openfilename_str
from src.utils.utils import ensure_parent_dir
from src.utils.helpers import clamp
from src.widgets.basik_widget import BasikWidget
from src.settings import themery as t
from src.utils import utils as u
from src.widgets.py_launcher import pylanes, kPaint, all_balls_fall, spacedits
from tkinter.ttk import Frame


CANVAS_SIZE = (128, 128)
SPIRITE_SIZE = (128, 128)

MINIMUM_SPRITE_OBJ_DICT = {
    'k_paint': {
        "player": "Brush"
    },
    "all_balls_fall": {
        "player": "Ball",
        "obstacle": "Platform"
    },
    "spaceDits": {
        "player": "Ship",
        "obstacle": "Asteroid",
        "enemy": "Alien"
    },
    "ThurBo": {
        "player": "Character",
        "obstacle": "Wall",
        "enemy": "Character",
        "collectable": "Coin"
    },
    "pylanes": {
        "player": "Character",
        "enemy": "Character"
    }
}

class Launchrr(BasikWidget):
    def __init__(self, width, height, master=None, tk_root_window=None):
        super().__init__(width, height, master)
        self.loaded_gaim = "all_balls_fall"
        self.loaded_gaim_string = "all_balls_fall"
        self.helper_commands['launch'] = [self.launch_gaim, "Launch the selected gaim from launchrr",
                                          {}, "GAIM", u.rgb_to_hex(t.JUNGLE_GREEN), u.rgb_to_hex(t.DARK_SEA_GREEN)]
        self.available_gaims = {
            'all_balls_fall': all_balls_fall.AllBallsFall,
            'k_paint': kPaint.Gaim,
            'spaceDits': spacedits.SpaceDits,
            'pylanes': pylanes.PyLanes
        }
        self.setup_dropdown_menus(list(self.available_gaims.keys()), dropdown_name="avail_gaims")
        self.setup_button_choices(["Save", "Load", "Launch"], start_y_cell=1)
        self.button_dict['Save'][1].config(command = lambda: self.save_gaim_profile())
        self.button_dict['Load'][1].config(command = lambda: self.load_gaim_profile())
        self.button_dict['Launch'][1].config(command = lambda: self.launch_gaim(self.dropdown_menu_dict['avail_gaims'][0].get()))
        self.launch_gaim_flag = False
        self.spirite_view_frames = {}
        self.setup_spirite_view_frames('all_balls_fall', get_min_spirite_obj_dict("all_balls_fall"))

    def clear_spirite_view_frames(self):
        for spirite_view_frame in self.spirite_view_frames.values():
            spirite_view_frame.grid_forget()
        self.spirite_view_frames = {}

    def setup_spirite_view_frames(self, game_name: str, spirite_dict: dict):
        self.clear_spirite_view_frames()
        s = 1
        for object_name, spirite_name in spirite_dict.items():
            new_view_frame = SpriteViewFrame(self, spirite_name)
            self.spirite_view_frames[object_name] = new_view_frame
            self.spirite_view_frames[object_name].grid(column=s, row=1, columnspan=4, rowspan=3)
            s += 5

    def launch_gaim(self, game_name: str = "all_balls_fall"):
        self.launch_gaim_flag = True
        self.loaded_gaim = self.available_gaims[game_name]
        self.loaded_gaim_string = game_name
        self.txo.priont_string(f"Loaded {game_name} and ready for launching..")

    def load_spirite_set(self, spirite_set: list):
        for spirite_name in spirite_set:
            shutil.copy(f"filesOutput/Bluebeard/spirites/{spirite_name}.png",
                        f"src/widgets/py_launcher/gaims/{self.loaded_gaim_string}/assets/{re.sub('[0-9]', '', spirite_name)}.png")

        self.txo.priont_string(f"Loaded spirite set {spirite_set}")

    def setup_dropdown_menus(self, word_list: Optional[List[str]]=None,
                             word_str: Optional[str]=None,
                             dropdown_name="",
                             start_x_cell=0,
                             start_y_cell=0):
        if word_list:
            if not hasattr(self, "dropdown_menu_dict"):
                self.dropdown_menu_dict = {}
            if not hasattr(self, "widget_display_array"):
                self.widget_display_array = []
            self.widget_display_array.append(dropdown_name)
            word_str_var = StringVar(value=word_list[0])
            self.dropdown_menu_dict[dropdown_name] = [
                word_str_var,
                OptionMenu(self, word_str_var, *word_list, command=self._on_gaim_changed)]
        # Add each dropdown menu to the artyle frame.
        for i, dropdown in enumerate(list(self.dropdown_menu_dict.keys())):
            row = i % 10
            col = i // 10
            self.dropdown_menu_dict[dropdown][1].grid(column=start_x_cell + col, row=start_y_cell + row)

    def _on_gaim_changed(self, selected_gaim: str):
        print(f"Gaim changed to {selected_gaim}")
        self.current_gaim = selected_gaim
        self.loaded_gaim = selected_gaim
        self.setup_spirite_view_frames(selected_gaim, get_min_spirite_obj_dict(selected_gaim))

    def save_gaim_profile(self):
        self.txo.priont_string("Saving gaim profile..")
        save_path = ensure_parent_dir(f"filesOutput/Bluebeard/.profiles/gaims/{self.loaded_gaim_string}_0000.json")
        json_dict = {}
        for spirite_name, spirite_view_frame in self.spirite_view_frames.items():
            json_dict[spirite_name] = spirite_view_frame.path_button.cget("text")
        with open(save_path, "w") as f:
            f.write(json.dumps(json_dict, indent=4, ensure_ascii=False))

    def load_gaim_profile(self):
        x = openfilename_str('filesOutput/Bluebeard/.profiles/gaims/')
        spirite_set = []
        with open(x, "r") as f:
            json_dict = json.load(f)
            for object_name, spirite_name in json_dict.items():
                spirite_set.append(spirite_name)
        x = x[len(os.getcwd()):]
        self.button_dict["Load"][0].set(x.split('/')[-1])
        self.load_spirite_set(spirite_set)


class SpriteViewFrame(Frame):
    def __init__(self, master=None, spirite_name="Ball"):
        super().__init__(master=master)
        self.spirite_name = spirite_name
        self.current_image = None
        self.spirite_number = 0
        self.spirite_number_range = (0, len(glob.glob(f"filesOutput/Bluebeard/spirites/{self.spirite_name}*.png"))-1)
        self._create_widgets()
        self._layout_widgets()
        self.update_display()

    def _create_widgets(self):
        self.layer_canvas = Canvas(self, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.layer_canvas.configure(bg="black")
        self.left_button = Button(self, text="<<", command=self.cycle_left, height=0, font=("Ariel", 8))
        self.right_button = Button(self, text=">>", command=self.cycle_right, height=0, font=("Ariel", 8))
        self.path_button = Button(self, text=f"/{self.spirite_name}{self.spirite_number}")


    def _layout_widgets(self):
        self.layer_canvas.grid(column=0, row=0, columnspan=4)
        self.path_button.grid(column=1, row=1, columnspan=2)
        self.left_button.grid(column=0, row=1)
        self.right_button.grid(column=3, row=1)


    def _get_path_text(self):
        """Generate the path text for the spirite canvas."""
        return f"{self.spirite_name}{self.spirite_number}"

    def cycle_left(self):
        self.spirite_number = clamp(
            self.spirite_number - 1,
            self.spirite_number_range[0],
            self.spirite_number_range[1],
            True)
        self.update_display()

    def cycle_right(self):
        self.spirite_number = clamp(
            self.spirite_number + 1,
            self.spirite_number_range[0],
            self.spirite_number_range[1],
            True)
        self.update_display()

    def update_display(self):
        """Update the display of the spirite canvas layer."""
        self.path_button.config(text=self._get_path_text())
        self._load_spirite_image()

    def _load_spirite_image(self):
        """Load the layer image from the spirite folder."""
        img = PhotoImage(file=f"filesOutput/Bluebeard/spirites/{self.spirite_name}{self.spirite_number}.png")
        self.current_image = img
        self.layer_canvas.delete("all")
        self.layer_canvas.create_image(CANVAS_SIZE[0]//2, CANVAS_SIZE[1]//2, image=self.current_image)
        # print(f"Loaded {img}")

    def set_spirite_info(self, spirite_name: str, layer_name: str):
        self.spirite_name = spirite_name
        self.update_display()

def get_min_spirite_obj_dict(game_name: str) -> dict:
    return MINIMUM_SPRITE_OBJ_DICT[game_name]