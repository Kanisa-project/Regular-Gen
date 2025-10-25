import os
import random
from tkinter import filedialog

# from pydub import AudioSegment
# from pydub.playback import play

import pygame.mixer

from src.settings import theme
from src.widgets import basik_widget, idutc
from src.widgets.texioty import texoty

"""
https://victormurcia.github.io/Making-Music-From-Images-in-Python/

HUUUUGE INSPIRATION
"""


class mujicPlayer(basik_widget.BasikWidget):
    def __init__(self, width, height, master=None, idutc_frame=None):
        super(mujicPlayer, self).__init__(master=master, width=width, height=height, text="Play Mujic: ")
        self.txo: texoty.TEXOTY = None
        self.idutc: idutc.IDUTC = idutc_frame
        pygame.mixer.init()

        self.setup_button_choices(["Change Mujic 1", "Change Mujic 2"])
        self.button_dict['Change Mujic 1'][1].configure(command=self.update_mujic_button)
        self.button_dict['Change Mujic 2'][1].configure(command=self.update_mujic2_button)
        self.helper_commands = {
            "play": [self.play_loaded_sound, "Plays whatever sound is loaded.",
                     {}, "MUJC", t.rgb_to_hex(t.LIGHT_WOOD), t.rgb_to_hex(t.VERY_DARK_BROWN)]
        }

        self.loaded_sound = pygame.mixer.Sound(f"filesInput/assets/Sounds/sound{random.randint(0, 9)}.wav")
        self.loaded_sound2 = pygame.mixer.Sound(f"filesInput/assets/Sounds/sound{random.randint(0, 9)}.wav")

    def play_loaded_sound(self, args: list):
        self.loaded_sound.play()
        self.loaded_sound2.play()

    def update_mujic_button(self):
        kre8dict = self.idutc.kre8dict
        x = ""
        rn = random.randint(0, 9)
        if kre8dict["artributes"][0] == "Random":
            x = f'/assets/Sounds/sound{rn}.wav'
        elif kre8dict["artributes"][0] == "Human":
            x = openfilename_str()
            x = x[len(os.getcwd()):]
        self.button_dict["Change Mujic 1"][0].set(x)
        self.loaded_wav_file = AudioSegment.from_wav(os.getcwd() + x)

    def update_mujic2_button(self):
        kre8dict = self.idutc.kre8dict
        x = ""
        rn = random.randint(0, 9)
        if kre8dict["artributes"][0] == "Random":
            x = f'/assets/Sounds/sound{rn}.wav'
        elif kre8dict["artributes"][0] == "Human":
            x = openfilename_str()
            x = x[len(os.getcwd()):]
        self.button_dict["Change Mujic 2"][0].set(x)
        self.loaded_wav_file2 = AudioSegment.from_wav(os.getcwd() + x)


def openfilename_str() -> str:
    filename = filedialog.askopenfilename(title='Open..')
    return filename
