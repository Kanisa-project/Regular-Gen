import random
from tkinter import *
from tkinter import ttk
import glyther
from PIL import Image, ImageDraw, ImageGrab

import idutc
import artay
import settings as s
import texoty


class KINVOW(ttk.LabelFrame):
    def __init__(self, width, height, master=None, idutc_frame=None, artay_frame=None):
        """
        Frame to show different options of different styles of art.
        
        :param width: Width of the Kinvow canvas.
        :param height: Height of the Kinvow canvas.
        :param master: Toolbox frame that contains each Tul.
        :param idutc_frame: Access to the IDUTC frame.
        :param artay_frame: Access to the ArTay frame.
        """
        super(KINVOW, self).__init__(master=master, width=width, height=height)

        # Initialize some Kinvow canvas variables.
        self.kinvow_img = None
        self.use_canvas = Canvas(self, bg=s.rgb_to_hex(s.RANDOM_COLOR3), width=width - 25, height=height - 25)
        self.use_canvas.grid(column=0, row=0, padx=3)
        self.canvas_w = width
        self.canvas_h = height

        # Configure the frame and grid settings.
        self.configure(text="Kinvow:  ")
        self.grid_propagate(False)

        # Setup other frames for access through-out the class.
        self.idutc: idutc.IDUTC = idutc_frame
        self.artay: artay.ARTAY = artay_frame

        # Start setup of Texioty.
        self.txo: texoty.TEXOTY = None
        self.texioty_commands = {
            "kin8": [self.create_masterpiece, "Create a masterpiece on Kinvow.",
                     ["glyth", "glyph", "wordie"], [], s.rgb_to_hex(s.LIGHT_GOLDENROD_YELLOW), s.rgb_to_hex(s.BLACK)],
            "kre8dict": [self.priont_kre8dict, "Show the creationary dictionary.",
                         [], [], s.rgb_to_hex(s.LIGHT_GOLDENROD_YELLOW), s.rgb_to_hex(s.BLACK)]
        }

    def priont_kre8dict(self, args):
        """
        Display the current kre8dict being used with a header.
        :param args:
        :return:
        """
        self.txo.clear_add_header()
        self.txo.priont_kre8dict(self.idutc.kre8dict)

    def create_masterpiece(self, args):
        """
        Create a masterpiece inside Kinvow with the selected options from the artyles selected by the kommand
        being used in Texoty.

        :return:
        """
        # Grab the correct and updated kre8dict and gather the options.
        kre8dict = self.idutc.kre8dict
        gather_options_dict = {'glyth': self.artay.glythTab.gather_glyth_options,
                               'glyph': self.artay.glyphTab.gather_glyph_options,
                               'wordie': self.artay.wordieTab.gather_wordie_options,
                               'spirite': self.artay.spiriteTab.gather_spirite_options,
                               'recipe': self.artay.recipeTab.gather_recipe_options,
                               'foto': self.artay.fotoTab.gather_foto_options,
                               'mujic': self.artay.mujicTab.gather_mujic_options,
                               'gaym': self.artay.gaymTab.gather_gaym_options,
                               'meem': self.artay.meemTab.gather_meem_options,
                               }

        # Cycle through each kommand argument to collect which options from which artyles.
        for mstr_pce in args:
            kre8dict[mstr_pce] = gather_options_dict[mstr_pce]()

        # Set the size of a new image to put the final masterpiece.
        size = (int(self.canvas_w) + 1, int(self.canvas_h) + 1)
        nim = Image.new("RGBA", size, s.DRS_PURPLE)

        # As long as there is at least one artyle, add the options of each artyle on the new image.
        if len(kre8dict) >= 1:
            self.create_artyles(nim, kre8dict, 'masterpiece', args)
            # Start creating the save path
            save_name = "_".join(args)
            save_path = f"{kre8dict['use_id']}/{save_name}.png"
            for c in save_path:
                if c in "?!&":
                    save_path = save_path.replace(c, "")
            # Save the created image and then place it inside Kinvow and add the file path to the kre8dict.
            nim.save(save_path)
            self.kinvow_img = PhotoImage(file=save_path)
            self.use_canvas.create_image(self.canvas_w // 2, self.canvas_h // 2, image=self.kinvow_img)
            kre8dict["file_path"] = save_path

    def create_artyles(self, nim, kre8dict, abt, args):
        """
        Decide which artyles to generate and create for display on Kinvow.

        :param nim: New image to place the creations.
        :param kre8dict: The dictionary of creation to use.
        :param abt: Avatar, Banner, Tile, Camel, Chicken, or Dawg?
        :param args: The Artyles to use from the kommand input from Texity
        :return:
        """
        for artyle in args:
            if artyle.lower() == "glyth":
                self.create_glyth(nim, kre8dict, abt)
            if artyle.lower() == "glyph":
                self.create_glyph(nim, kre8dict, abt)
            if artyle.lower() == "wordie":
                self.create_wordie(nim, kre8dict, abt)
            if artyle.lower() == "spirite":
                self.create_spirite(nim, kre8dict, abt)
            if artyle.lower() == "foto":
                self.create_foto(nim, kre8dict, abt)
            if artyle.lower() == "recipe":
                self.create_recipe(nim, kre8dict, abt)
            if artyle.lower() == "mujic":
                self.create_mujic(nim, kre8dict, abt)
            if artyle.lower() == "gaym":
                self.create_gaym(nim, kre8dict, abt)

    def create_glyth(self, img: Image, kre8dict: dict, abt="masterpiece"):
        self.artay.glythTab.add_glyth(img, kre8dict, abt)

    def create_glyph(self, img: Image, kre8dict: dict, abt="masterpiece"):
        self.artay.glyphTab.add_glyph(img, kre8dict, abt)

    def create_wordie(self, img: Image, kre8dict: dict, abt='masterpiece'):
        self.artay.wordieTab.add_wordie(img, kre8dict, abt)

    def create_spirite(self, img: Image, kre8dict: dict, abt='masterpiece'):
        self.artay.spiriteTab.add_spirite(img, kre8dict, abt)

    def create_foto(self, img: Image, kre8dict: dict, abt='masterpiece'):
        self.artay.fotoTab.add_foto(img, kre8dict, abt)

    def create_recipe(self, img: Image, kre8dict: dict, abt='masterpiece'):
        self.artay.recipeTab.add_recipe(img, kre8dict, abt)

    def create_mujic(self, img: Image, kre8dict: dict, abt='masterpiece'):
        self.artay.mujicTab.add_mujic(img, kre8dict, abt)

    def create_gaym(self, img: Image, kre8dict: dict, abt='masterpiece'):
        self.artay.gaymTab.add_gaym(img, kre8dict, abt)

    def set_pen_masterpiece(self, args) -> dict:
        """
        Create a single letter ID and a 10-digit UTC masterpiece with artyles as normally.
        :param args: Should contain a single letter and a 10-digit number.
        :return:
        """
        # Set up the pen kre8dict and available artyles.
        kanisa_pen_dict = self.idutc.setup_kre8dict(args[0], args[1])
        kanisa_pen_dict['artributes'] = self.idutc.gather_random_attributes()
        random_artyles = []
        possible_artyles = ["glyth", "glyph", "wordie", "recipe", "spirite"]
        random_options_dict = {'glyth': self.artay.glythTab.gather_random_options,
                               'glyph': self.artay.glyphTab.gather_random_options,
                               'wordie': self.artay.wordieTab.gather_random_options,
                               'spirite': self.artay.spiriteTab.gather_random_options,
                               'recipe': self.artay.recipeTab.gather_random_options}
        # Pick 3 random artyles and run their creations.
        for i in range(3):
            random_artyles.append(random.choice(possible_artyles))
        for ran_artyle in random_artyles:
            kanisa_pen_dict[ran_artyle] = random_options_dict[ran_artyle]()
        # Add Loopring minting requirements.
        kanisa_pen_dict.update(self.txo.master.helper_dict["LAPI"][0].attach_pen_min_reqs(args))

        # Upload the masterpiece Pen to Pinata IPFS and update the pen kre8dict.
        ipfs_pen = self.create_pen_image(kanisa_pen_dict)
        kanisa_pen_dict['image'] += ipfs_pen
        kanisa_pen_dict['animation_url'] += ipfs_pen
        kanisa_pen_dict['collection_metadata'] += "0xd3c9d6d7d5cd249069d5f46f136357c0c2bd189b"
        # Save the pen dictionary.
        self.idutc.save_json_pen(kanisa_pen_dict)
        return kanisa_pen_dict

    def make_pencilcase(self, args):
        """
        Create a set of single letter masterpiece files meant to create a full masterpiece that can be rendered
        in a Kanisa Render.
        :param args: First arg should be (a-z) or (0-9) and second arg a 10-digit number.
        :return:
        """
        if args[0] == 'a-z' and args[1].length == 10:
            for char in 'abcdefghijklmnopqrstuvwxyz':
                pen_dict = self.set_pen_masterpiece([char, args[1]])
                # self.create_pen_image([char, "2367418095"])
                self.idutc.save_json_pen(pen_dict)
        elif args[0] == '0-9' and args[1].length == 10:
            for char in '0123456789':
                pen_dict = self.set_pen_masterpiece([char, args[1]])
                # self.create_pen_image([char, "2367418095"])
                self.idutc.save_json_pen(pen_dict)

    def create_pen_image(self, penDict: dict) -> str:
        """
        Create a Kinvow image for a single character masterpiece.

        :param penDict: Single letter kre8dict masterpiece.
        :return:
        """
        save_path = ''
        nim = Image.new("RGBA", (64, 64), s.DRS_PURPLE)
        save_name = penDict['use_id'] + "_" + penDict['use_utc']
        if len(penDict) >= 1:
            self.create_artyles(nim, penDict, 'masterpiece', list(penDict.keys()))
            save_path = f"kanisaPens/{save_name}.png"
            for c in save_path:
                if c in "?!&":
                    save_path = save_path.replace(c, "")
            nim.save(save_path)
            # self.kinvow_img = PhotoImage(file=save_path)
            # self.use_canvas.create_image(self.canvas_w // 2, self.canvas_h // 2, image=self.kinvow_img)
        ipfs_pen_hash = self.txo.master.helper_dict["PAPI"][0].pin_pen_image(save_path, save_name)
        penDict["file_path"] = save_path
        return ipfs_pen_hash
