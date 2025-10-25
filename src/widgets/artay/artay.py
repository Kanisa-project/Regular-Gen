import random
from tkinter import ttk

from src.settings import themery as t
from src.widgets.texioty import texoty
from src.widgets.artay import tab_mujic, tab_spirite, tab_glyth, tab_recipe, tab_foto, tab_gaim, tab_wordie, tab_meem, tab_glyph

FONT_NAMES = ["Parkinsans-Medium", "rogue", "Cookie-Regular", "berkshireswash-regular",
              "Akt", "AguafinaScript-Regular", "Charlie", "fontello", "CodygoonRegular-oweO0",
              "Gisshiri-4nLDD", "Ancientsans-rvyrK", "MertalionPersonalUseOnlyReg-V4D0V", "SuboleyaRegular-qZeV1",
              "Jemgonzademo-lgRqw", "Stars-DEa1", "MintsodaLimeGreen13X16Regular-KVvzA", "PixgamerRegular-OVD6A",
              "Monofur-PK7og", "AnonymousPro-2O73w"]


class ARTAY(ttk.LabelFrame):
    def __init__(self, width, height, master=None, idutc_frame=None):
        """
        An array of art. A few styles turns into alot of styles. Maybe too many styles, possibly not enough.
        The world may never know.
        
        :param master: aRtay frame, housing all the other artay.
        """

        super(ARTAY, self).__init__(master, width=int(width), height=int(height))
        self.config(text="aRtay:  ")
        self.IDUTC_frame = idutc_frame
        self.grid_propagate(False)
        self.txo: texoty.TEXOTY = None

        self.tabControl = ttk.Notebook(self, width=int(width), height=int(height))
        self.glythTab = tab_glyth.Glyther(master=self.tabControl,
                                          width=int(width), height=int(height))
        self.glyphTab = tab_glyph.Glyphin(master=self.tabControl,
                                          width=int(width), height=int(height))
        self.spiriteTab = tab_spirite.Spirite(master=self.tabControl,
                                              width=int(width), height=int(height))
        self.wordieTab = tab_wordie.Wordie(master=self.tabControl,
                                           width=int(width), height=int(height), kinvow_size=(620, 940))
        self.recipeTab = tab_recipe.AlaNFT(master=self.tabControl,
                                           width=int(width), height=int(height))
        self.fotoTab = tab_foto.Fotoes(master=self.tabControl,
                                       width=int(width), height=int(height))
        self.mujicTab = tab_mujic.Mujic(master=self.tabControl,
                                        width=int(width), height=int(height))
        self.gaimTab = tab_gaim.Gaim(master=self.tabControl,
                                     width=int(width), height=int(height))
        self.meemTab = tab_meem.Meem(master=self.tabControl,
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
        self.helper_commands = {
            "glyth": [self.change_glyth, "Add glyth options to the kre8dict.",
                      {"add": "Add a glyth to the kre8dict.",
                       "new": "Make a new option for glyth."}, "ARTY", t.rgb_to_hex(t.LIGHT_GOLDENROD_YELLOW),
                      t.rgb_to_hex(t.DARK_SEA_GREEN)],
            "glyph": [self.change_glyph, "Add glyph options to the kre8dict.",
                      {"add": "Add a glyph to the kre8dict.",
                       "new": "Make a new option for glyph."}, "ARTY", t.rgb_to_hex(t.LIGHT_GOLDENROD_YELLOW),
                      t.rgb_to_hex(t.DARK_SEA_GREEN)],
            "wordie": [self.change_wordie, "Change wordie options and choices.",
                       {"add": "Add a wordie type to the kre8dict.",
                        "font": "Select which font for Kinvow to use."}, "ARTY", t.rgb_to_hex(t.LIGHT_GOLDENROD_YELLOW),
                       t.rgb_to_hex(t.DARK_SEA_GREEN)],
            "recipe": [self.change_recipe, "Change recipe options and choices.",
                       {"add": "Add a recipe to the kre8dict.",
                        "new": "Make a new recipe for the book."}, "ARTY", t.rgb_to_hex(t.LIGHT_GOLDENROD_YELLOW),
                       t.rgb_to_hex(t.DARK_SEA_GREEN)],
            "spirite": [self.change_spirite, "Change spirite options and choices.",
                        {"add": "Add a spirite to the kre8dict.",
                         "new": "Import a new set of spirite layers."}, "ARTY", t.rgb_to_hex(t.LIGHT_GOLDENROD_YELLOW),
                        t.rgb_to_hex(t.DARK_SEA_GREEN)]
        }

    def change_glyth(self, args: list):
        self.txo.priont_string(f"Glything up a {args}")
        if "add" in args:
            self.IDUTC_frame.kre8dict["glyth"] = self.glythTab.command_glyth_options(
                command_arg=str(random.randint(1, 3)))
            if len(args) == 2:
                self.IDUTC_frame.kre8dict["glyth"] = self.glythTab.command_glyth_options(command_arg=args[1])

        elif "new" in args:
            self.glythTab.checkbutton_dict["FUCK YEAH"] = []

    def change_glyph(self, args: list):
        self.txo.priont_string(f"Glyphing on a {args}")
        if "add" in args:
            self.IDUTC_frame.kre8dict["glyph"] = self.glyphTab.command_glyph_options(
                command_arg=str(random.randint(1, 3)))
            if len(args) == 2:
                self.IDUTC_frame.kre8dict["glyph"] = self.glyphTab.command_glyph_options(command_arg=args[1])

    def change_wordie(self, args: list):
        self.txo.priont_string(f"Wordifying on the {args}")
        if "font" in args:
            self.txo.master.start_question_prompt(
                {"confirming_function": ["Which font to use?", "", str(random.randint(0, 10)), self.change_font]},
                clear_txo=True)
            self.txo.priont_string(
                f"Current font: {FONT_NAMES.index(self.wordieTab.font_name)} - {self.wordieTab.font_name}")
            self.txo.priont_list(FONT_NAMES, parent_key="Fonts", numbered=True)
        elif "add" in args:
            self.IDUTC_frame.kre8dict["wordie"] = self.wordieTab.command_wordie_options(
                command_arg=str(random.randint(1, 3)))
            if len(args) == 2:
                self.IDUTC_frame.kre8dict["wordie"] = self.wordieTab.command_wordie_options(command_arg=args[1])

    def change_recipe(self, args: list):
        self.txo.priont_string(f"Whipping with the {args}")
        if 'add' in args:
            self.IDUTC_frame.kre8dict["recipe"] = self.recipeTab.command_recipe(
                random.choice(["casseroles", "other", "desserts", "soups", "seasonings"]))
            if len(args) == 2:
                self.IDUTC_frame.kre8dict['recipe'] = self.recipeTab.command_recipe(args[1])
        elif 'new' in args and len(args) >= 2:
            if "OSRS" in args:
                self.recipeTab.add_osrs_tab()

    def change_spirite(self, args):
        self.txo.priont_string(f"Spiriting within {args}")
        if 'add' in args:
            self.IDUTC_frame.kre8dict['spirite'] = self.spiriteTab.command_spirite(random.choice(["Asteroid", "Alien", "Ship", "Medallion"]))
            if len(args) == 2:
                self.IDUTC_frame.kre8dict['spirite'] = self.spiriteTab.command_spirite(args[1])

    def change_mujic(self, args: list):
        pass

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

    def change_font(self, font_digit: int):
        self.wordieTab.font_name = FONT_NAMES[font_digit]
        self.txo.priont_string(f"Newly loaded font {font_digit} - {FONT_NAMES[font_digit]}")
