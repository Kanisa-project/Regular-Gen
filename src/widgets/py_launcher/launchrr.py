from src.widgets.basik_widget import BasikWidget
from src.settings import themery as t, utils as u
from src.widgets.texioty.helpers.tex_helper import TexiotyHelper


class Launchrr(BasikWidget):
    def __init__(self, width, height, master=None, tk_root_window=None):
        super().__init__(width, height, master)
        self.helper_commands['launch'] = [self.launch_gaim, "Launch the selected gaim from launchrr",
                                          {}, "GAIM", u.rgb_to_hex(t.JUNGLE_GREEN), u.rgb_to_hex(t.DARK_SEA_GREEN)]
        self.setup_dropdown_menus(["kPaint", "pylanes"])
        self.setup_button_choices(["Launch"], start_y_cell=1)
        self.button_dict['Launch'][1].config(command=self.launch_gaim)
        self.root_win = tk_root_window

    def launch_gaim(self, game_name: str = "kPaint"):
        self.txo.priont_string(f"Launching {game_name}..")
        self.root_win._launch_game_request = True
        print("Setted it to TRUE")
