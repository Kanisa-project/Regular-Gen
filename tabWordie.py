import os
import random
from tkinter import *
import artstyle
import wordie
from settings import *
from tkinter import ttk

import wtabHangman
import wtabCrossword
import wtabWordSearch
import wtabRiddle
import wtabCollage


class Wordie(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        """
        This artyle has everything to do with words and how they correlate to each other or lack there of. It can be a
        riddle or a crossword. It could be a game of hangman as a riddle or some lyrics mixed together. Mad libs or mad
        gabs or word search. The list is as endless as your imagination, really.

        :param master: aRtay frame, housing all the other artyles.
        :param idutc: idutc frame, user input frame.
        """
        super(Wordie, self).__init__(master=master, idutc=idutc, width=width, height=height)
        # Set up the name and add the possible choices.
        self.tab_name = "Wordie"
        self.idutc_frame = idutc
        self.wordie_choices = ["Collage", "Riddle", "Word Search", "Hangman", "Crossword"]
        self.setup_radiobutton_choices(self.wordie_choices)
        self.wordieBook = ttk.Notebook(master=self)
        self.hangmanTab = wtabHangman.Hangman(master=self.wordieBook)
        self.wordsearchTab = wtabWordSearch.WordSearch(master=self.wordieBook)
        self.crosswordTab = wtabCrossword.Crossword(master=self.wordieBook)
        self.riddleTab = wtabRiddle.Riddle(master=self.wordieBook)
        self.collageTab = wtabCollage.Collage(master=self.wordieBook)

        self.wordieBook.add(self.collageTab, text="Collage")
        self.wordieBook.add(self.riddleTab, text="Riddle")
        self.wordieBook.add(self.wordsearchTab, text="Word Search")
        self.wordieBook.add(self.hangmanTab, text="Hangman")
        self.wordieBook.add(self.crosswordTab, text="Crossword")

        self.wordieBook.grid(row=0, column=1, rowspan=6)

    def destroy_word_optionmenus(self):
        """
        Destroy each of the optionmenus that contain wordlists. Unsure of exactly what is going on here.
        """
        for c in self.optionmenu_dict:
            self.optionmenu_dict[c][1].destroy()

    def gather_wordie_options(self) -> dict:
        """
        Gather and return a dictionary of wordie options, such as the type of art it is. Hangman, poem, random sentence
        generator. Along with the phrase for hangman or list of words in a word search or crossword.
        """
        chosen_wordie_options = {
            "type": self.radiobutton_dict["Collage"][0].get()
        }
        if self.radiobutton_dict["Collage"][0].get() == 0:
            chosen_wordie_options["Collage"] = {}
            for i, word in enumerate(self.collageTab.textbox_dict):
                chosen_wordie_options["Collage"][word] = self.collageTab.textbox_dict[word][0].get()
        if self.radiobutton_dict["Riddle"][0].get() == 1:
            chosen_wordie_options["Riddle"] = {}
            for i, word in enumerate(self.riddleTab.textbox_dict):
                chosen_wordie_options["Riddle"][word] = self.riddleTab.textbox_dict[word][0].get()
        if self.radiobutton_dict["Word Search"][0].get() == 2:
            chosen_wordie_options["Word Search"] = {}
            for i, word in enumerate(self.wordsearchTab.textbox_dict):
                chosen_wordie_options["Word Search"][str(i)] = self.wordsearchTab.textbox_dict[word][0].get()
        if self.radiobutton_dict["Hangman"][0].get() == 3:
            chosen_wordie_options["Hangman"] = {
                'Phrase': self.hangmanTab.textbox_dict["Phrase"][0].get(),
                'Max Guesses': self.hangmanTab.max_guesses
            }
        if self.radiobutton_dict["Crossword"][0].get() == 4:
            chosen_wordie_options["Crossword"] = {
                "Across": self.crosswordTab.across_hint_dict,
                "Down": self.crosswordTab.down_hint_dict
            }
        return chosen_wordie_options

    def gather_random_options(self) -> dict:
        """
        Select some random wordie options.
        :return:
        """
        chosen_wordie_options = {
            "type": random.choice(self.wordie_choices)
        }
        return chosen_wordie_options

    def add_wordie(self, img: Image, kre8dict: dict, abt="masterpiece") -> Image:
        """
        Adds the wordie type of wordie on the img provided.
        """
        # Set up the colors being used to display in the Kinvow.
        artribute_dict = self.set_artributes(kre8dict)
        if kre8dict["wordie"]["type"] == 0:
            kre8dict["wordie"]["type"] = "Collage"
            wordie.kollage(img, artribute_dict, kre8dict["wordie"]["Collage"])
        if kre8dict["wordie"]["type"] == 1:
            kre8dict["wordie"]["type"] = "Riddle"
            wordie.riddler(img, artribute_dict, kre8dict["wordie"]["Riddle"])
        if kre8dict["wordie"]["type"] == 2:
            kre8dict["wordie"]["type"] = "Word Search"
            wordie.word_search(img, artribute_dict, kre8dict["wordie"]["Word Search"])
        if kre8dict["wordie"]["type"] == 3:
            kre8dict["wordie"]["type"] = "Hangman"
            wordie.hangman(img, artribute_dict, kre8dict["wordie"]["Hangman"])
        if kre8dict["wordie"]["type"] == 4:
            kre8dict["wordie"]["type"] = "Crossword"
            wordie.crossword(img, artribute_dict, kre8dict["wordie"]["Crossword"])

        return img

    # def add_wordie(self, img: Image, kre8dict: dict, abt="masterpiece") -> Image:
    #     """
    #     Adds the wordie type of wordie on the img provided.
    #     """
    #     # Set up the colors being used to display in the Kinvow.
    #     artribute_dict = self.set_artributes(kre8dict)
    #
    #     # IF SELECTED POSITION IS 0, IT IS A HANGMAN WORDIE
    #     if kre8dict["wordie"]["type"] == 0:
    #         kre8dict["wordie"]["type"] = "hangman"
    #         kre8dict["wordie"]["hangman"] = {
    #             "chosen": random.choice(kre8dict["artributes"]),
    #             "hidden": {},
    #             "missed_letters": []
    #         }
    #         for c in kre8dict["wordie"]["hangman"]["chosen"]:
    #             if c in kre8dict["wordie"]["hangman"]["hidden"]:
    #                 c += c
    #             kre8dict["wordie"]["hangman"]["hidden"][c] = "◙"
    #         wordie.hangman(img, kre8dict)
    #
    #     # IF SELECTED POSITION IS 1, IT IS A WORD_SEARCH WORDIE
    #     if kre8dict["wordie"]["type"] == 1:
    #         kre8dict["wordie"]["type"] = "word_search"
    #         kre8dict["wordie"]["word_search"] = {
    #             "letter_array": [],
    #             "word_list": [],
    #             'found_words': []
    #         }
    #         wordie.word_search(img, kre8dict)
    #
    #     # IF SELECTED POSITION IS 2, IT IS A COLLAGE WORDIE
    #     if kre8dict["wordie"]["type"] == 2:
    #         kre8dict["wordie"]["type"] = "collage"
    #         wordie.kollage(img, kre8dict)
    #
    #     return img

    # def create_werd_serch(self, kre8dict: dict):
    #     for filename in os.listdir(f"WORDIE/"):
    #         if filename.startswith("index"):
    #             print(filename)
    #             line_list = []
    #             with open(f"WORDIE/{filename}", "r") as file:
    #                 for line in file.readlines():
    #                     line_list.append(line)
    #             with open(f"WORDIE/{kre8dict['use_id']}{filename}", "w") as file:
    #                 for line in line_list:
    #                     if line.find("letters_grid = ~~[]~~") >= 0:
    #                         print(kre8dict["wordie"])
    #                         line = line.replace("letters_grid = ~~[]~~", f"letters_grid = {kre8dict['Wordie']['Word Search']['Letter Array']}")
    #                     if line.find("word_array = ~~[]~~") >= 0:
    #                         print("THIS")
    #                         line = line.replace("word_array = ~~[]~~", f"word_array = {kre8dict['Wordie']['Word Search']['Word List']}")
    #                     file.write(line)
