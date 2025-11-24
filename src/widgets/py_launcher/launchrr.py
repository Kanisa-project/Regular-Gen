import glob
from tkinter import Canvas, Button, OptionMenu, StringVar, PhotoImage
from typing import Optional, List

from src.utils.helpers import clamp
from src.widgets.basik_widget import BasikWidget
from src.settings import themery as t
from src.services import utils as u
from src.widgets.py_launcher import pylanes, kPaint, all_balls_fall, spacedits
from tkinter.ttk import Frame


CANVAS_SIZE = (128, 128)
SPIRITE_SIZE = (128, 128)

MINIMUM_SPRITE_OBJ_DICT = {
    "ABF": {
        "player": "Ball",
        "obstacle": "Platform"
    },
    "spaceDits": {
        "player": "Ship",
        "enemy": "Alien",
        "obstacle": "Asteroid"
    }
}

class Launchrr(BasikWidget):
    def __init__(self, width, height, master=None, tk_root_window=None):
        super().__init__(width, height, master)
        self.loaded_gaim = None
        self.helper_commands['launch'] = [self.launch_gaim, "Launch the selected gaim from launchrr",
                                          {}, "GAIM", u.rgb_to_hex(t.JUNGLE_GREEN), u.rgb_to_hex(t.DARK_SEA_GREEN)]
        self.available_gaims = {
            'ABF': all_balls_fall.AllBallsFall,
            'k_paint': kPaint.Gaim,
            'spaceDits': None,
            'pylanes': pylanes.PyLanes
        }
        self.setup_dropdown_menus(list(self.available_gaims.keys()), dropdown_name="avail_gaims")
        self.setup_button_choices(["Launch"], start_x_cell=1)
        # self.spirite_view_frame = SpriteViewFrame(self)
        # self.spirite2_view_frame = SpriteViewFrame(self, "Platform")
        # self.spirite_view_frame.grid(column=0, row=1, columnspan=4)
        # self.spirite2_view_frame.grid(column=5, row=1, columnspan=4)
        self.button_dict['Launch'][1].config(command = lambda: self.launch_gaim(self.dropdown_menu_dict['avail_gaims'][0].get()))
        self.launch_gaim_flag = False
        self.spirite_view_frames = []

    def setup_spirite_selections(self, gaim_name: str):
        for gaim_object in get_min_spirite_obj_dict(gaim_name):
            self.spirite_view_frame.set_spirite_info(get_min_spirite_obj_dict(gaim_name)[gaim_object], gaim_object)
            self.spirite2_view_frame.set_spirite_info(get_min_spirite_obj_dict(gaim_name)[gaim_object], gaim_object)

    def launch_gaim(self, game_name: str = "ABF"):
        self.launch_gaim_flag = True
        self.loaded_gaim = self.available_gaims[game_name]
        self.txo.priont_string(f"Loaded {game_name} and ready for launching..")

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
        self.setup_spirite_selections(selected_gaim)


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