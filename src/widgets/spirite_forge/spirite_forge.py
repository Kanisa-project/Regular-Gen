import glob
import random
from tkinter import *
from tkinter import ttk
from typing import List, Dict, Optional

from PIL import Image

from ..artay.tab_foto import openfilename_str
from ..basik_widget import BasikWidget
from ...features.artay import spirite
from src.utils.utils import rgb_to_hex, load_idutc
from ...settings.app_settings import LAYER_DICT
from ...utils.helpers import clamp

MAX_LAYERS = 4
LAYER_NUMBER_RANGE = (0, 9)
CANVAS_SIZE = (128, 128)
SPIRITE_SIZE = (128, 128)

ARTRIMOJI = {
    "Door": '🚪',
    "Window": '🪟',
    "Cloud": '☁',
    "Rainbow": '🌈',
    "Fire": '🔥',
    "Ice": '🧊',
    "Camel": '🐫',
    "Chicken": '🐓',
    "Rock": '🗿',
    "Sock": '🧦',
    "Crayon": '🖍',
    "Pen": '🖋',
    "Confetti": '🎊',
    "Mosaic": '🧱',
    "Butterfly": '🦋',
    "Sponge": '🧽',
    "Metal": '🛡️',
    "Petal": '🌷',
    "Printer": '🖨️',
    "Stamp": '📠'
}

class IDUTCpalette(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.grid_propagate = False
        self.current_idutc = None

    def change_idutc(self, new_idutc: dict):
        self.update_color_palette(new_idutc['color_list'])
        # self.update_emoji_palette(new_idutc['artributes'])

    def update_color_palette(self, color_list: List[tuple]):
        for colo in color_list:
            colo_button = Button(self, bg=rgb_to_hex(colo))
            colo_button.grid(column=color_list.index(colo)%4, row=color_list.index(colo)%2)
            # colo_button.bind('<Button-3>', lambda event, col=colo: self.change_idutc(col))

    def update_emoji_palette(self, emoji_list: dict):
        emoji_list = list(emoji_list.keys())
        for emoj in emoji_list:
            emoj_button = Button(self, text=ARTRIMOJI[emoj], font=('Ariel', 5))
            emoj_button.grid_propagate = False
            emoj_button.grid(column=emoji_list.index(emoj)%3, row=(emoji_list.index(emoj)%2)+2)


class SpiriteLayerFrame(ttk.Frame):
    def __init__(self, master=None, spirite_name="Ball", layer_name="Base"):
        super().__init__(master=master)
        self.spirite_name = spirite_name
        self.layer_name = layer_name
        self.current_image = None
        self.layer_number = 0
        self.frame_number = 0
        self.palette = IDUTCpalette(self)
        self._create_widgets()
        self._layout_widgets()
        self.update_display()

    def _create_widgets(self):
        self.layer_canvas = Canvas(self, width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.layer_canvas.configure(bg="black")
        self.left_button = Button(self, text="<<", command=self.cycle_left, height=0, font=("Ariel", 8))
        self.right_button = Button(self, text=">>", command=self.cycle_right, height=0, font=("Ariel", 8))
        self.path_button = Button(self, text=f"/{self.spirite_name}/{self.layer_name}{self.layer_number}")


    def _layout_widgets(self):
        self.layer_canvas.grid(column=0, row=0, columnspan=4)
        self.path_button.grid(column=1, row=1, columnspan=2)
        self.left_button.grid(column=0, row=1)
        self.right_button.grid(column=3, row=1)
        self.palette.grid(column=0, row=3, columnspan=4)


    def _get_path_text(self):
        """Generate the path text for the spirite canvas."""
        return f"{self.layer_name}{self.layer_number}"

    def cycle_left(self):
        self.layer_number = clamp(
            self.layer_number - 1,
            LAYER_NUMBER_RANGE[0],
            LAYER_NUMBER_RANGE[1],
            True)
        self.update_display()

    def cycle_right(self):
        self.layer_number = clamp(
            self.layer_number + 1,
            LAYER_NUMBER_RANGE[0],
            LAYER_NUMBER_RANGE[1],
            True)
        self.update_display()

    def update_display(self):
        """Update the display of the spirite canvas layer."""
        self.path_button.config(text=self._get_path_text())
        self._load_layer_image()

    def _load_layer_image(self):
        """Load the layer image from the spirite folder."""
        img = spirite.load_spirite_layer(self.spirite_name, self.layer_name, self.layer_number)
        self.current_image = img
        self.layer_canvas.delete("all")
        self.layer_canvas.create_image(CANVAS_SIZE[0]//2, CANVAS_SIZE[1]//2, image=self.current_image)
        # print(f"Loaded {img}")

    def set_spirite_info(self, spirite_name: str, layer_name: str):
        self.spirite_name = spirite_name
        self.layer_name = layer_name
        self.update_display()

class SpiriteLayerManager:
    def __init__(self, master, num_layers: int=MAX_LAYERS):
        self.master = master
        self.layer_frames: List[SpiriteLayerFrame] = []
        self._create_layer_frames(num_layers)

    def _create_layer_frames(self, num_layers: int):
        for i in range(num_layers):
            frame = SpiriteLayerFrame(master=self.master)
            frame.grid(column=i, row=(i%2)+1, columnspan=2)
            self.layer_frames.append(frame)

    def update_all_layers(self, spirite_name: str, layer_names: List[str]):
        for i, frame in enumerate(self.layer_frames):
            if i < len(layer_names):
                frame.set_spirite_info(spirite_name, layer_names[i])
                # frame.palette.change_idutc(self.master.current_idutc_dict)

    def randomize_all_layers(self):
        for frame in self.layer_frames:
            frame.layer_number = random.randint(*LAYER_NUMBER_RANGE)
            frame.update_display()

    def get_layer_configuration(self) -> List[Dict]:
        return [
            {
                'name': frame.layer_name,
                'number': frame.layer_number,
                'spirite': frame.spirite_name
            }
            for frame in self.layer_frames
        ]


class SpiriteForge(BasikWidget):
    AVAILABLE_SPIRITES = [
        "None", "Alien", "Asteroid", "Ball", "Medallion", "Ship", "Sword",
        "Tribloc", "RTJ", "Boat", "Platform", "Goal"]
    def __init__(self, width, height, master=None):
        """
        A tab with options for loading different spirite layers. First select a spirit you would like to turn into a
        sprite, and then select the various different layers or have the computer make a random one.

        :param master: aRtay frame, housing all the other artay.
        """
        super().__init__(master=master, width=int(width), height=height)
        self.tab_name = "Spirite"
        self.current_spirite = "Ball"
        self.layer_definitions = LAYER_DICT.get(self.current_spirite, {})
        self.current_idutc_dict = load_idutc(random.choice(glob.glob("filesOutput/Bluebeard/.idutc/*.json")))

        self._setup_spirite_selector()
        self.setup_button_choices(["Randomize layers"], start_x_cell=1)
        self.setup_button_choices(["Change IDUTC"], start_x_cell=2)
        self.setup_button_choices(["Save Spirite"], start_x_cell=3)
        self.button_dict["Randomize layers"][1].configure(command=self.randomize_all_layers)
        self.button_dict["Change IDUTC"][1].configure(command=self.choose_idutc_dialog)
        self.button_dict["Change IDUTC"][1].bind('<Button-3>', self.get_random_idutc)
        self.button_dict["Save Spirite"][1].configure(command=self.save_spirite)
        self.layer_manager = SpiriteLayerManager(self)

        self._update_layer_display()

    def _setup_spirite_selector(self):
        self.setup_dropdown_menus(
            word_list=self.AVAILABLE_SPIRITES,
            dropdown_name="spirite_type")
        if "spirite_type" in self.dropdown_menu_dict:
            self.dropdown_menu_dict["spirite_type"][0].set(self.current_spirite)


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
                OptionMenu(self, word_str_var, *word_list, command=self._on_spirite_changed)]
        # Add each dropdown menu to the artyle frame.
        for i, dropdown in enumerate(list(self.dropdown_menu_dict.keys())):
            row = i % 10
            col = i // 10
            self.dropdown_menu_dict[dropdown][1].grid(column=start_x_cell + col, row=start_y_cell + row)

    def _on_spirite_changed(self, selected_spirite: str):
        print(f"Spirite changed to {selected_spirite}")
        self.current_spirite = selected_spirite
        self.layer_definitions = LAYER_DICT.get(self.current_spirite, {})
        self._update_layer_display()

    def _update_layer_display(self):
        layer_names = list(self.layer_definitions.keys())
        self.layer_manager.update_all_layers(self.current_spirite, layer_names)

    def get_spirite_configuration(self) -> Dict:
        layer_config = self.layer_manager.get_layer_configuration()
        return {
            'spirite_type': self.current_spirite,
            'layers': layer_config,
            'spirite_definition': self.layer_definitions
        }

    def get_random_configuration(self) -> Dict:
        selected_spirite = random.choice(self.AVAILABLE_SPIRITES)
        return {
            'spirite_type': selected_spirite,
            'spirite_definition': LAYER_DICT.get(selected_spirite, {})
        }

    def get_command_configuration(self, spirite_name: str) -> Dict:
        spirite_name = spirite_name.title()
        if spirite_name not in LAYER_DICT:
            raise ValueError(f"Spirite {spirite_name} not found.")
        layer_names = list(LAYER_DICT[spirite_name].keys())
        layer_config = []
        for layer_name in layer_names[:MAX_LAYERS]:
            layer_config.append({
                'name': layer_name,
                'number': random.randint(*LAYER_NUMBER_RANGE)
            })
        return {
            'spirite_type': spirite_name,
            'layers': layer_config,
            'spirite_definition': LAYER_DICT[spirite_name]
        }

    def randomize_all_layers(self):
        self.layer_manager.randomize_all_layers()

    def add_spirite_to_image(self, img: Image.Image, config_dict: Dict,
                             description: str = 'masterpiece') -> Image.Image:
        try:
            artributes = self.set_artributes(config_dict)
            artributes['spirite'] = config_dict.get('spirite', config_dict.get('spirite'))

            width, height = img.size
            spirite_image = spirite.stack_layers(img, artributes, SPIRITE_SIZE)
            spirite_x = (width // 2) - (SPIRITE_SIZE[0] // 2)
            spirite_y = (height // 2) - (SPIRITE_SIZE[1] // 2)

            img.paste(spirite_image, (spirite_x, spirite_y), mask=spirite_image)
            return img

        except Exception as e:
            return img

    def gather_spirite_options(self) -> dict:
        pass


    def get_random_idutc(self, event=None):
        rando_idutc = random.choice(glob.glob("filesOutput/Bluebeard/.idutc/*.json"))
        self.button_dict["Change IDUTC"][0].set(rando_idutc[len("filesOutput/Bluebeard/.idutc/"):].replace("_", "\n"))
        # self.current_idutc = load_idutc(self.button_dict["Change IDUTC"][0].get())


    def choose_idutc_dialog(self):
        full_idutc_path = openfilename_str("filesOutput/Bluebeard/.idutc/")
        # x = full_idutc_path[len("filesOutput/Bluebeard/.idutc/"):]
        split_path = full_idutc_path.split('/')
        idutc_name = split_path[-1]
        self.button_dict["Change IDUTC"][0].set(idutc_name.replace("_", "\n"))
        self.current_idutc_dict = load_idutc("filesOutput/Bluebeard/.idutc/"+idutc_name)
        self._update_layer_display()

    def save_spirite(self):
        spirite_visual_config = self.get_spirite_configuration()|self.current_idutc_dict
        spirite_img = spirite.stack_layers(Image.new("RGBA", (1, 1)), spirite_visual_config, (64, 64))
        spirite_num = len(glob.glob(f"filesOutput/Bluebeard/spirites/{self.current_spirite}*.png"))
        spirite_img.save(f"filesOutput/Bluebeard/spirites/{self.current_spirite}{spirite_num}.png")
