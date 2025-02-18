import os
import random
import tkinter as tk
from tkinter import filedialog

from pydub import AudioSegment
from pydub.playback import play

import helper_widget
import idutc
import settings as s
import texoty

"""
https://victormurcia.github.io/Making-Music-From-Images-in-Python/

HUUUUGE INSPIRATION
"""


class mujicPlayer(helper_widget.helpingWidget):
    def __init__(self, width, height, master=None, idutc_frame=None):
        super(mujicPlayer, self).__init__(master=master, width=width, height=height, text="Play Mujic: ")
        self.txo: texoty.TEXOTY = None
        self.idutc: idutc.IDUTC = idutc_frame
        self.setup_button_choices(["Change Mujic 1", "Change Mujic 2"])
        self.button_dict['Change Mujic 1'][1].configure(command=self.update_mujic_button)
        self.button_dict['Change Mujic 2'][1].configure(command=self.update_mujic2_button)
        self.texioty_commands = {
            "play": [self.play_loaded_sound, "Plays whatever sound is loaded.",
                     {}, "MUJC", s.rgb_to_hex(s.LIGHT_WOOD), s.rgb_to_hex(s.VERY_DARK_BROWN)]
        }

        self.loaded_wav_file = AudioSegment.from_wav(f"assets\Sounds\sound{random.randint(0, 9)}.wav")
        self.loaded_wav_file2 = AudioSegment.from_wav(f"assets\Sounds\sound{random.randint(0, 9)}.wav")

    def play_loaded_sound(self, args: list):
        overlay = self.loaded_wav_file.overlay(self.loaded_wav_file2, position=0)
        play(overlay)
        pass

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
