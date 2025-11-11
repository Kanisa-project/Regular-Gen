from src.widgets.basik_widget import BasikWidget
from src.settings import themery as t
from src.services import utils as u
from src.widgets.py_launcher import pylanes, kPaint


class Launchrr(BasikWidget):
    def __init__(self, width, height, master=None, tk_root_window=None):
        super().__init__(width, height, master)
        self.loaded_gaim = None
        self.helper_commands['launch'] = [self.launch_gaim, "Launch the selected gaim from launchrr",
                                          {}, "GAIM", u.rgb_to_hex(t.JUNGLE_GREEN), u.rgb_to_hex(t.DARK_SEA_GREEN)]
        self.available_gaims = {
            'k_paint': kPaint.Gaim,
            'pylanes': pylanes.PyLanes
        }
        self.setup_dropdown_menus(list(self.available_gaims.keys()))
        self.setup_button_choices(["Launch"], start_y_cell=1)
        self.button_dict['Launch'][1].config(command=self.launch_gaim)
        self.launch_gaim_flag = False

    def launch_gaim(self, game_name: str = "k_paint"):
        self.txo.priont_string(f"Launching {game_name}..")
        self.launch_gaim_flag = True
        self.loaded_gaim = self.available_gaims[game_name]
        print("Setted it to TRUE")
