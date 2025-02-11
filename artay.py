import random
from tkinter import *
from tkinter import ttk

import tabFoto
import tabGaim
import tabGlyth
import tabGlyph
import tabMeem
import tabMujic
import tabRecipe
import tabWordie
import tabSpirite
import settings as s
import texoty

FONT_NAMES = ["Parkinsans-Medium", "rogue", "Cookie-Regular", "berkshireswash-regular",
              "Akt-Medium", "AguafinaScript-Regular", "Charlie", "fontello", "CodygoonRegular-oweO0",
              "Gisshiri-4nLDD", "Ancientsans-rvyrK", "MertalionPersonalUseOnlyReg-V4D0V", "SuboleyaRegular-qZeV1",
              "Jemgonzademo-lgRqw", "Stars-DEa1", "MintsodaLimeGreen13X16Regular-KVvzA", "PixgamerRegular-OVD6A",
              "Monofur-PK7og", "AnonymousPro-2O73w"]


class ARTAY(ttk.LabelFrame):
    def __init__(self, width, height, master=None, idutc_frame=None):
        """
        An array of art. A few styles turns into alot of styles. Maybe too many styles, possibly not enough.
        The world may never know.
        
        :param master: aRtay frame, housing all the other artyles.
        """

        super(ARTAY, self).__init__(master, width=int(width), height=int(height))
        self.config(text="aRtay:  ")
        self.IDUTC_frame = idutc_frame
        # self.mp_img = None
        self.grid_propagate(False)
        self.txo: texoty.TEXOTY = None

        self.tabControl = ttk.Notebook(self, width=int(width), height=int(height))
        self.glythTab = tabGlyth.Glyther(master=self.tabControl, idutc=self.IDUTC_frame,
                                         width=int(width), height=int(height))
        self.glyphTab = tabGlyph.Glyphin(master=self.tabControl, idutc=self.IDUTC_frame,
                                         width=int(width), height=int(height))
        self.spiriteTab = tabSpirite.Spirite(master=self.tabControl, idutc=self.IDUTC_frame,
                                             width=int(width), height=int(height))
        self.wordieTab = tabWordie.Wordie(master=self.tabControl, idutc=self.IDUTC_frame,
                                          width=int(width), height=int(height))
        self.recipeTab = tabRecipe.AlaNFT(master=self.tabControl, idutc=self.IDUTC_frame,
                                          width=int(width), height=int(height))
        self.fotoTab = tabFoto.Fotoes(master=self.tabControl, idutc=self.IDUTC_frame,
                                      width=int(width), height=int(height))
        self.mujicTab = tabMujic.Mujic(master=self.tabControl, idutc=self.IDUTC_frame,
                                       width=int(width), height=int(height))
        self.gaimTab = tabGaim.Gaim(master=self.tabControl, idutc=self.IDUTC_frame,
                                    width=int(width), height=int(height))
        self.meemTab = tabMeem.Meem(master=self.tabControl, idutc=self.IDUTC_frame,
                                    width=int(width), height=int(height))
        self.tabControl.add(self.glythTab, text="Glyth")
        self.tabControl.add(self.glyphTab, text="Glyph")
        self.tabControl.add(self.wordieTab, text="Wordie")
        self.tabControl.add(self.spiriteTab, text="Spirite")
        self.tabControl.add(self.recipeTab, text="Recipe")
        self.tabControl.add(self.fotoTab, text="Foto")
        self.tabControl.add(self.mujicTab, text="Mujic")
        self.tabControl.add(self.gaimTab, text="Gaim")
        self.tabControl.add(self.meemTab, text="Meem")
        self.tabControl.grid(column=0, row=0)
        self.texioty_commands = {
            "wordie": [self.change_wordie_font, "Change wordie options and choices.",
                       {"0-9": "Number of Wordies to make.",
                        "font": "Select a new font for Kinvow to use."}, [], s.rgb_to_hex(s.MUSTARD_YELLOW),
                       s.rgb_to_hex(s.DARK_SEA_GREEN)]
        }

        # self.texioty_commands = {
        #     # "add_recipe": [self.add_recipe_to_tab, "Add Glyth options to the kre8dict.",
        #     #           {"0-9": "Number of Glyth to make."}, [], s.rgb_to_hex(s.BLACK), s.rgb_to_hex(s.LIGHT_GOLDENROD_YELLOW)],
        #     "glyph": [self.draw_on_kinvow, "Add Glyph options to the kre8dict.",
        #               {"0-9": "Number of Glyph to make."}, [], s.rgb_to_hex(s.BLACK), s.rgb_to_hex(s.LIGHT_GOLDENROD_YELLOW)]
        # }

    def change_wordie_font(self, args: list):
        if "font" in args:
            self.txo.priont_list(FONT_NAMES, parent_key="Fonts--", numbered=True)
            self.txo.master.start_question_prompt({"font_digit": ["Which font to use?", "", str(random.randint(0, 10))]},
                                                  clear_txo=False)
            if self.txo.master.response_dict['font_digit'][1]:
                self.wordieTab.font_name = FONT_NAMES[int(self.txo.master.response_dict['font_digit'][1])]

    def draw_on_kinvow(self, num):
        pass

    def add_osrs_recipes(self):
        if self.IDUTC_frame.kre8dict["data_source"] == "OSRS":
            self.recipeTab.add_osrs_tab()

    def random_kre8shun(self):
        """Random data source means super random stuff, not a data source chosen at random."""
        pass

    def reddit_kre8shun(self):
        """A text post from reddit with all sorts of fun things."""
        pass

    def osrs_kre8shun(self):
        """Decorative skill-menu art stuff and whatnot."""
        pass

    def human_kre8shun(self):
        """Not quite sure yet."""
        pass

    def mtg_kre8shun(self):
        """MTG Deck creation. Randomized deck for maximum fun."""
        pass

    def barcode_kre8shun(self):
        """Barcode artwork. Think about it."""
        pass

    def add_recipe_to_tab(self, args):
        pass
