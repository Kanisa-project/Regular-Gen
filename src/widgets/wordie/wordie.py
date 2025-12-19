from tkinter import *
from tkinter import ttk

from .categories import wtabCrossword, wtabWordSearch, wtabCollage, wtabHangman, wtabRiddle
from ..basik_widget import BasikWidget
# from ...features.artay import categories


class Wordie(BasikWidget):
    def __init__(self, width, height, master=None, idutc=None, kinvow_size=(0, 0)):
        """
        This artyle has everything to do with words and how they correlate to each other or lack there of. It can be a
        riddle or a crossword. It could be a game of hangman as a riddle or some lyrics mixed together. Mad libs or mad
        gabs or word search. The list is as endless as your imagination, really.

        :param master: aRtay frame, housing all the other artay.
        :param idutc: idutc frame, user input frame.
        """
        super(Wordie, self).__init__(master=master, width=width, height=height)
        # Set up the name and add the possible choices.
        self.tab_name = "Wordie"
        self.idutc_frame = idutc
        self.font_name = "Akt"

        self.wordieBook = ttk.Notebook(master=self)
        self.hangmanTab = wtabHangman.Hangman(master=self.wordieBook, width=width, height=height, text="Hangman")
        self.wordsearchTab = wtabWordSearch.WordSearch(master=self.wordieBook, width=width, height=height)
        self.crosswordTab = wtabCrossword.Crossword(master=self.wordieBook, width=width, height=height)
        self.riddleTab = wtabRiddle.Riddle(master=self.wordieBook, width=width, height=height)
        self.collageTab = wtabCollage.Collage(master=self.wordieBook, masterpiece_size=kinvow_size, width=width, height=height)

        self.wordieBook.add(self.collageTab, text="Collage")
        self.wordieBook.add(self.riddleTab, text="Riddle")
        self.wordieBook.add(self.wordsearchTab, text="Word Search")
        self.wordieBook.add(self.hangmanTab, text="Hangman")
        self.wordieBook.add(self.crosswordTab, text="Crossword")

        self.wordieBook.grid(row=0, column=1, rowspan=6)

    def gather_wordie_options(self, command_arg='') -> dict:
        """
        Gather and return a dictionary of categories options, such as the type of art it is. Hangman, poem, random sentence
        generator. Along with the phrase for hangman or list of words in a word search or crossword.
        """
        chosen_wordie_options = {
            "type": self.wordieBook.index('current')
        }
        if self.wordieBook.index('current') == 0:
            canvas_points = self.collageTab.get_graph_canvas_points()
            chosen_wordie_options["Collage"] = {}
            for i, word in enumerate(self.collageTab.textbox_dict):
                chosen_wordie_options["Collage"][word] = [self.collageTab.textbox_dict[word][0].get(), canvas_points[word][0], canvas_points[word][1], canvas_points[word][2],
                                                          canvas_points[word][3], canvas_points[word][4]]
        elif self.wordieBook.index('current') == 1:
            chosen_wordie_options["Riddle"] = {}
            for i, word in enumerate(self.riddleTab.textbox_dict):
                chosen_wordie_options["Riddle"][word] = self.riddleTab.textbox_dict[word][0].get()
        elif self.wordieBook.index('current') == 2:
            chosen_wordie_options["Word Search"] = {}
            for i, word in enumerate(self.wordsearchTab.textbox_dict):
                chosen_wordie_options["Word Search"][str(i)] = self.wordsearchTab.textbox_dict[word][0].get()
        elif self.wordieBook.index('current') == 3:
            chosen_wordie_options["Hangman"] = {
                'Phrase': self.hangmanTab.textbox_dict["Phrase"][0].get(),
                'Max Guesses': self.hangmanTab.max_guesses
            }
        elif self.wordieBook.index('current') == 4:
            chosen_wordie_options["Crossword"] = {
                "Across": self.crosswordTab.across_hint_dict,
                "Down": self.crosswordTab.down_hint_dict
            }

        return chosen_wordie_options

    def gather_random_options(self) -> dict:
        """
        Select some random categories options.
        :return:
        """
        chosen_wordie_options = {
            "type": random.choice(self.wordie_choices)
        }
        return chosen_wordie_options

    def add_wordie(self, img: Image, kre8dict: dict, abt="masterpiece") -> Image:
        """
        Adds the categories type of categories on the img provided.
        """
        # Set up the colors being used to display in the Kinvow.
        wordie.FONT_NAME = self.font_name
        # print(categories.FONT_NAME, " = ", self.font_name)
        artribute_dict = self.set_artributes(kre8dict)
        if kre8dict["categories"]["type"] == 0:
            kre8dict["categories"]["type"] = "Collage"
            wordie.kollage(img, artribute_dict, kre8dict["categories"]["Collage"])
        if kre8dict["categories"]["type"] == 1:
            kre8dict["categories"]["type"] = "Riddle"
            wordie.riddler(img, artribute_dict, kre8dict["categories"]["Riddle"])
        if kre8dict["categories"]["type"] == 2:
            kre8dict["categories"]["type"] = "Word Search"
            wordie.word_search(img, artribute_dict, kre8dict["categories"]["Word Search"])
        if kre8dict["categories"]["type"] == 3:
            kre8dict["categories"]["type"] = "Hangman"
            hangman(img, artribute_dict, kre8dict["categories"]["Hangman"])
        if kre8dict["categories"]["type"] == 4:
            kre8dict["categories"]["type"] = "Crossword"
            wordie.crossword(img, artribute_dict, kre8dict["categories"]["Crossword"])

        return img
    # def create_werd_serch(self, kre8dict: dict):
    #     """Template replacer, I believe."""
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
    #                         print(kre8dict["categories"])
    #                         line = line.replace("letters_grid = ~~[]~~", f"letters_grid = {kre8dict['Wordie']['Word Search']['Letter Array']}")
    #                     if line.find("word_array = ~~[]~~") >= 0:
    #                         print("THIS")
    #                         line = line.replace("word_array = ~~[]~~", f"word_array = {kre8dict['Wordie']['Word Search']['Word List']}")
    #                     file.write(line)
