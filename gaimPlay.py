import random
import tkinter as tk

import idutc
import settings as s
import texoty
import wtabHangman as hm
import casino as cas


class gaimPlayer(tk.LabelFrame):
    def __init__(self, width, height, master=None, idutc_frame=None):
        super(gaimPlayer, self).__init__(master, width=width, height=height, text="PlayGaim: ")
        self.txo: texoty.TEXOTY = None
        self.idutc: idutc.IDUTC = idutc_frame
        self.inGaim = False
        self.width = width
        self.height = height
        self.loaded_gaim = "Hangman"
        self.hangman_hidden_dict = {}
        self.player_stay = False
        self.blackjack_hand = []
        self.dealer_hand = []
        self.blackjack_value = 0
        self.dealer_value = 0
        # self.suits = "♠♡♣♢"
        # self.CARD_DECK = {
        #     "♠": ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
        #     "♡": ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
        #     "♣": ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'],
        #     "♢": ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        #
        # }
        self.is_playing = False

        self.texioty_commands = {
            "play": [self.start_gaim, "Play a gaim from the Masterpiece.",
                     {"hangman": "Guess the phrase one letter at time.",
                      "blackjack": "Play some blackjack behind the casino."}, [], s.rgb_to_hex(s.LIGHT_STEEL_BLUE),
                     s.rgb_to_hex(s.DARK_GREEN_COPPER)],
            # "enter": [self.enter_area, 'Enter an area for "multiplayer".',
            #           {"casino": "Gamble against someone.",
            #            "thunderdome": "Welcome to the thunderdome, %profile_name%."}, [],
            #           s.rgb_to_hex(s.LIGHT_STEEL_BLUE),
            #           s.rgb_to_hex(s.DARK_GREEN_COPPER)],
            "guess": [self.guess_play, "Guess a letter for Hangman.",
                      {}, [], s.rgb_to_hex(s.LIGHT_STEEL_BLUE),
                      s.rgb_to_hex(s.DARK_GREEN_COPPER)],
            "blackjack": [self.black_jack_play, "Make a blackjack play.",
                          {"hit": "Take another card in blackjack.",
                           "stay": "Stay with your cards in blackjack."}, [], s.rgb_to_hex(s.LIGHT_STEEL_BLUE),
                          s.rgb_to_hex(s.DARK_GREEN_COPPER)]
        }

    def start_gaim(self, args):
        print("starting gaim", self.idutc.kre8dict)
        if "hangman" in args:
            try:
                if "Hangman" == self.idutc.kre8dict["wordie"]["type"]:
                    self.loaded_gaim = "Hangman"
                    self.inGaim = True
                    self.start_hangman(self.idutc.kre8dict["wordie"]['Hangman'])
            except KeyError as e:
                raise KeyError("Ain't got the key, dawg")
        elif "blackjack" in args:
            self.loaded_gaim = "Blackjack"
            self.inGaim = True
            self.start_blackjack()
        else:
            raise PermissionError("Don't have hangman, bub.")

    def quit_gaim(self, args):
        pass

    def enter_area(self):
        pass

    def start_hangman(self, hangman_dict: dict):
        hm.missed_letters = []
        phrase = hangman_dict['Phrase']
        max_misses = hangman_dict["Max Guesses"]
        hm.gaim_phrase = phrase
        hm.max_guesses = max_misses
        self.hangman_hidden_dict = phrase_to_hidden_dict(phrase)
        self.txo.clear_add_header("Hangman")
        self.txo.priont_string(hm.HANGMAN_TEXTMAN_LIST[0])
        self.txo.priont_string(dict_to_str(self.hangman_hidden_dict))

    # def process_gaimplay(self, args):
    #     print("Process", args)
    #     if self.loaded_gaim == "Hangman":
    #         pass

    def guess_play(self, args):
        if self.inGaim:
            self.txo.clear_add_header("Hangman")
            if len(args[0]) == 1:
                self.hangman_hidden_dict = hm.check_hangman_letter(args[0], self.hangman_hidden_dict)
            self.txo.priont_string(hm.HANGMAN_TEXTMAN_LIST[s.clamp(len(hm.missed_letters), 0, 6)])
            self.txo.priont_string(dict_to_str(self.hangman_hidden_dict))
            self.txo.priont_list(hm.missed_letters, parent_key="\nMissed")
            self.hangman_gaimover_check()

    def hangman_gaimover_check(self):
        if len(hm.missed_letters) >= 6:
            self.inGaim = False
            self.txo.priont_string("Dang, so close")
            self.txo.priont_string(hm.gaim_phrase)
        elif "◙" not in list(self.hangman_hidden_dict.values()):
            self.inGaim = False
            self.txo.priont_string("Congratulations!!!!")

    def black_jack_play(self, args):
        if "hit" in args:
            new_card = cas.draw_a_card()
            self.blackjack_hand.append(cas.apply_card_template(new_card[0]))
            self.blackjack_value += new_card[1]
        elif "stay" in args:
            self.player_stay = True
        self.display_dealer_hand()
        self.display_player_hand()

    def display_dealer_hand(self):
        self.txo.clear_add_header()
        if self.player_stay:
            new_card = cas.draw_a_card()
            self.dealer_hand.append(cas.apply_card_template(new_card[0]))
            self.txo.priont_string(self.dealer_hand[0])
            self.txo.priont_string(self.dealer_hand[1])
            self.dealer_value += new_card[1]
            self.txo.priont_string(f"Dealer has: {self.dealer_value}")
        else:
            self.txo.priont_string(cas.FACE_DOWN_TEMPLATE)
            self.txo.priont_string(self.dealer_hand[0])
            self.txo.priont_string(f"Dealer showing: {self.dealer_value}")

    def display_player_hand(self):
        self.txo.priont_break_line()
        for card in self.blackjack_hand:
            self.txo.priont_string(card)
        self.txo.priont_string(f"Hand value: {self.blackjack_value}")

    def start_blackjack(self):
        new_card1 = cas.draw_a_card()
        new_card3 = cas.draw_a_card()
        new_card4 = cas.draw_a_card()
        self.blackjack_hand.append(cas.apply_card_template(new_card1[0]))
        self.blackjack_hand.append(cas.apply_card_template(new_card3[0]))
        self.dealer_hand.append(cas.apply_card_template(new_card4[0]))
        self.blackjack_value += new_card1[1]
        self.blackjack_value += new_card3[1]
        self.dealer_value += new_card4[1]
        self.display_dealer_hand()
        self.display_player_hand()


def dict_to_str(hidden_word_dict: dict) -> str:
    hidden_word_str = ""
    for c in list(hidden_word_dict.keys()):
        print(c, hidden_word_dict[c])
        hidden_word_str += hidden_word_dict[c]
    return hidden_word_str


def phrase_to_hidden_dict(phrase: str) -> dict:
    print(phrase)
    hidden_phrase_dict = {}
    for c in phrase:
        while c in hidden_phrase_dict:
            c += c[0]
        if c[0].lower() not in "abcdefghijklmnopqrstuvwxyz":
            hidden_phrase_dict[c] = c[0]
        else:
            hidden_phrase_dict[c] = "◙"
    return hidden_phrase_dict
