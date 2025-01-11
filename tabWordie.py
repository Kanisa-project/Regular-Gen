import os
import random
from tkinter import *
import artstyle
import wordie
from settings import *


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
        self.tab_name = "wordie"
        self.wordie_choices = ["hangman", "word_search", "collage", "riddle"]
        self.setup_radiobutton_choices(self.wordie_choices)

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
        # Needs to not be used with a 'word_search' key.
        chosen_wordie_options = {
            "type": self.radiobutton_dict["word_search"][0].get()
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
        selected_colors = []
        if kre8dict["artributes"][1] == "Rainbow":
            for ltr in kre8dict["use_id"]:
                selected_colors.append(ALPHANUMERIC_COLORS[ltr])
        elif kre8dict["artributes"][1] == "Cloud":
            shadelvl = 255 // len(kre8dict["use_id"])
            for i in range(len(kre8dict["use_id"])):
                selected_colors.append(((i + 1) * shadelvl, (i + 1) * shadelvl, (i + 1) * shadelvl))

        # IF SELECTED POSITION IS 0, IT IS A HANGMAN WORDIE
        if kre8dict["wordie"]["type"] == 0:
            kre8dict["wordie"]["type"] = "hangman"
            kre8dict["wordie"]["hangman"] = {
                "chosen": random.choice(kre8dict["artributes"]),
                "hidden": {},
                "missed_letters": []
            }
            for c in kre8dict["wordie"]["hangman"]["chosen"]:
                if c in kre8dict["wordie"]["hangman"]["hidden"]:
                    c += c
                kre8dict["wordie"]["hangman"]["hidden"][c] = " ◙ "
            wordie.hangman(img, kre8dict)

        # IF SELECTED POSITION IS 1, IT IS A WORD_SEARCH WORDIE
        if kre8dict["wordie"]["type"] == 1:
            kre8dict["wordie"]["type"] = "word_search"
            kre8dict["wordie"]["word_search"] = {
                "letter_array": [],
                "word_list": [],
                'found_words': []
            }
            wordie.word_search(img, kre8dict)

        # IF SELECTED POSITION IS 2, IT IS A COLLAGE WORDIE
        if kre8dict["wordie"]["type"] == 2:
            kre8dict["wordie"]["type"] = "collage"
            wordie.kollage(img, kre8dict)

        return img

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
                        # if line.find("word_array = ~~[]~~") >= 0:
                        #     print("THIS")
                        #     line = line.replace("word_array = ~~[]~~", f"word_array = {kre8dict['Wordie']['Word Search']['Word List']}")
                        # file.write(line)
