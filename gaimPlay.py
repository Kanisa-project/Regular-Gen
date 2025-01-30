import tkinter as tk
import settings as s
import texoty
import wtabHangman as hm


class gaimPlayer(tk.LabelFrame):
    def __init__(self, width, height, master=None):
        super(gaimPlayer, self).__init__(master, width=width, height=height, text="PlayGaim: ")
        self.txo: texoty.TEXOTY = None
        self.width = width
        self.height = height
        self.loaded_gaim = "Hangman"
        self.hangman_hidden_dict = {}
        self.is_playing = False

        self.texioty_commands = {
            "play": [self.start_gaim, "Play a gaim from the Masterpiece.",
                     {"hangman": "Guess the phrase one letter at time.",
                      "blackjack": "Play some blackjack behind the casino."}, [], s.rgb_to_hex(s.LIGHT_STEEL_BLUE),
                     s.rgb_to_hex(s.DARK_GREEN_COPPER)],
            "enter": [self.enter_area, 'Enter an area for "multiplayer".',
                      {"casino": "Gamble against someone.",
                       "thunderdome": "Welcome to the thunderdome, %profile_name%."}, [],
                      s.rgb_to_hex(s.LIGHT_STEEL_BLUE),
                      s.rgb_to_hex(s.DARK_GREEN_COPPER)],
            "guess": [self.guess_play, "Guess a letter for Hangman.",
                      {}, [], s.rgb_to_hex(s.LIGHT_STEEL_BLUE),
                      s.rgb_to_hex(s.DARK_GREEN_COPPER)]
        }

    def start_gaim(self, args):
        print(args)
        if "hangman" in args:
            self.loaded_gaim = "Hangman"
            self.start_hangman(args)
        elif "blackjack" in args:
            pass

    def quit_gaim(self, args):
        pass

    def enter_area(self):
        pass

    def start_hangman(self, args):
        self.hangman_hidden_dict = phrase_to_hidden_dict("It's just a phrase.")
        self.txo.priont_string(hm.HANGMAN_TEXTMAN_LIST[0])
        self.txo.priont_string(dict_to_str(self.hangman_hidden_dict))

    # def process_gaimplay(self, args):
    #     print("Process", args)
    #     if self.loaded_gaim == "Hangman":
    #         pass

    def guess_play(self, args):
        print("guess:", args)
        if len(args[0]) == 1:
            hm.check_hangman_letter(args[0])
            self.txo.priont_string(str(args))


def dict_to_str(hidden_word_dict: dict) -> str:
    hidden_word_str = ""
    for c in hidden_word_dict:
        hidden_word_str += hidden_word_dict[c]
    return hidden_word_str


def phrase_to_hidden_dict(phrase: str) -> dict:
    hidden_phrase_dict = {}
    for c in phrase:
        if c in hidden_phrase_dict:
            c += c
        hidden_phrase_dict[c] = "◙"
    return hidden_phrase_dict
