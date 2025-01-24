import random
from tkinter import *
from tkinter import ttk

import tabFoto
import tabGaym
import tabGlyth
import tabGlyph
import tabMeem
import tabMujic
import tabRecipe
import tabWordie
import tabSpirite


class ARTAY(ttk.LabelFrame):
    def __init__(self, width, height, master=None, idutc_frame=None):
        """
        An array of art. A few styles turns into alot of styles. Maybe too many styles, possibly not enough.
        The world may never know.
        
        :param master: aRtay frame, housing all the other artyles.
        """

        super(ARTAY, self).__init__(master, width=int(width), height=int(height))
        self.config(text="aRtay")
        self.IDUTC_frame = idutc_frame
        # self.mp_img = None
        self.grid_propagate(False)

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
        self.gaymTab = tabGaym.Gaym(master=self.tabControl, idutc=self.IDUTC_frame,
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
        self.tabControl.add(self.gaymTab, text="Gaym")
        self.tabControl.add(self.meemTab, text="Meem")
        self.tabControl.grid(column=0, row=0)

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
