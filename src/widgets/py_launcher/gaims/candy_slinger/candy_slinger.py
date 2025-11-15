from src.widgets.py_launcher.gaims.base_gaim.base_gaim import BaseGaim
from src.widgets.texioty.gaims.candy_slinger import CandySlingerRunner


class CandySlinger(BaseGaim, CandySlingerRunner):
    def __init__(self, player_name):
        BaseGaim.__init__(self, player_name)
