import os
import random
from tkinter import *

from PIL import Image
from PIL import ImageTk
import shutil
import artstyle
import gaym
import spirite
from settings import *
import codecs


class Gaym(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        super(Gaym, self).__init__(master=master, idutc=idutc, width=width, height=height)
        self.disp_img = None
        self.tab_name = "gaym"
        self.gaym_optionmenu_choice_list = ["SpaceDits", "ABF", "ThurBo", "Othaido", "BootyDefence"]
        # self.spirite_option_dict = {
        #     "Othaido": ["RTJ", "Boat"],
        #     "SpaceDits": ["Alien", "Ship", "Asteroid"],
        #     "ABF": ["Ball", "Platform"],
        #     "ThurBo": ["Sword", "Tribloc"],
        #     "Booty Race": ["Boat", "RTJ"],
        # }
        # self.update_gaym_spirites_button = Button(self, text="Update", command=self.generate_populate_spirite_choices)
        # self.update_gaym_spirites_button.grid(column=0, row=1)
        self.spirite_type_str_var = StringVar()
        self.spirite_type_str_var.set("ABF")
        spirite_type_dropmenu = OptionMenu(self, self.spirite_type_str_var, *self.gaym_optionmenu_choice_list)
        spirite_type_dropmenu.grid(column=0, row=0)

        self.gaym_sheet_index_dict = {
            "A": ["Player", "player", "Enemy", "Ally"],
            "B": ["Obstacle", "Goal", "Collectible", "Portal"],
            "C": ["Obstacle", "Goal", "Collectible", "Portal"],
            "D": ["Obstacle", "Goal", "Collectible", "Portal"],
        }

        self.gaym_sheet_dict = {
            "A": {},
            "B": {},
            "C": {},
            "D": {}
        }
        ci = 0
        ri = 0

        for ltr, options_list in self.gaym_sheet_index_dict.items():
            for col_num in range(3):
                ltr_str_var = StringVar()
                ltr_str_var.set(random.choice(options_list))
                self.gaym_sheet_dict[ltr][str(col_num)] = []
                self.gaym_sheet_dict[ltr][str(col_num)].append(ltr_str_var)
                self.gaym_sheet_dict[ltr][str(col_num)].append(OptionMenu(self, ltr_str_var, *options_list))
                if ci > 2:
                    ci -= 3
                    ri += 1
                self.gaym_sheet_dict[ltr][str(col_num)][1].grid(column=ci + 1, row=ri + 1)
                ci += 1

    def gather_gaym_options(self) -> dict:
        """
        Gather and return options for factor lists, spirites and rule sets.

        @return:
        """
        chosen_gaym_options = {}
        for ltr, chosen_options in self.gaym_sheet_dict.items():
            chosen_gaym_options[ltr] = {}
            for nbr, option_choice in chosen_options.items():
                chosen_gaym_options[ltr][nbr] = option_choice[0].get()
        chosen_gaym_options["gaym_play"] = self.spirite_type_str_var.get()
        chosen_gaym_options["MovementProfile"] = random.choice(["LR", "UD"])
        if chosen_gaym_options["gaym_play"] == "ABF":
            chosen_gaym_options["MovementProfile"] = "LR"
        return chosen_gaym_options

    def generate_populate_spirite_choices(self):
        # print(self.gaym_sheet_dict["A"]["1"][0].get())
        self.destroy_word_optionmenus()
        self.setup_dropdown_menus()

    def destroy_word_optionmenus(self):
        """Destroy each of the optionmenus that contain wordlists"""
        # print(self.gaym_sheet_dict)
        for ltr in self.gaym_sheet_dict:
            for nbr in self.gaym_sheet_dict[ltr]:
                self.gaym_sheet_dict[ltr][nbr][1]['menu'].delete("0", END)
                # self.gaym_sheet_dict[ltr][nbr][1].destroy()

    # def setup_wordlist_optionmenus(self):
    #     """Create optionmenus for each wordlist."""
    #     ci = 0
    #     ri = 0
    #     for ltr in self.gaym_sheet_index_dict:
    #         for nbr in self.gaym_sheet_index_dict[ltr]:
    #             print(ltr, nbr)
    #             self.gaym_sheet_dict[ltr][nbr][0].set(list(self.gaym_sheet_dict[ltr].keys())[0])
    #             self.gaym_sheet_dict[ltr][nbr].append(OptionMenu(self, self.gaym_sheet_dict[ltr][nbr][0],
    #                                                              *list(self.gaym_sheet_dict[ltr].keys())))
    #             if ci > 3:
    #                 ci -= 4
    #                 ri += 1
    #             self.gaym_sheet_dict[ltr][nbr][1].grid(column=ci + 1, row=ri + 1)
    #             ci += 1

    # def create_gaym(self, kre8dict: dict):
    #     """
    #     Create spirite sheet for a gaym.
    #     :return:
    #     """
    #     img = self.create_spirite_sheet(kre8dict)
    #     self.disp_img = ImageTk.PhotoImage(img)
    #     kre8dict["Canvas"].create_image(0, 0, image=self.disp_img)
    #     for ltr in kre8dict["gaym"]:
    #         for nbr in range(4):
    #             fraim = stack_layers(kre8dict["gaym"][ltr][nbr], kre8dict["number_list"], kre8dict["color_list"])
    #     self.create_spirite(kre8dict, slot_pos=(xw, yh))

    def create_spirite_sheet(self, img: Image, kre8dict: dict) -> Image:
        """Create a game sprite using PNGs"""
        # nim = Image.new('RGBA', (640, 640), (0, 0, 0, 0))
        w, h = img.size
        iw, ih = 128, 128
        yh = 0
        for ltr in ['A', 'B', 'C', 'D']:

            for nbr in range(3):
                print("POKL", kre8dict["gaym"][ltr][str(nbr)])
                fraim = self.stack_layers(kre8dict["gaym"][ltr][str(nbr)], kre8dict["number_list"],
                                          kre8dict["color_list"], (iw, ih))
                img.paste(fraim, (nbr * iw, yh * ih), mask=fraim)
                # fraim = fraim.resize((64, 64))
                # fraim.save(f'GAYM/{kre8dict["artributes"][3]}/{kre8dict["name"]}/{ltr}{nbr}_'
                #            f'{kre8dict["gaym"][ltr][nbr]}.png')
            yh += 1
        return img

    def add_gaym(self, img: Image, kre8dict: dict, abt='masterpiece') -> Image:
        # gaym.create_directory(img, kre8dict, gaym_str=kre8dict["gaym"]["gaym_play"])

        # for filename in os.listdir(f"GAYM/Components/BTNassets"):
        #     if filename.endswith(".png"):
        #         print(filename)
        #         shutil.copy("GAYM/Components/BTNassets/"+filename, f"GAYM/{kre8dict['artributes'][3]}/{kre8dict['name']}/BTNassets/{filename[:-4]}.png")
        # for filename in os.listdir(f"GAYM/Components/"):
        #     if filename.endswith(".py"):
        #         line_list = []
        #         with open(f"GAYM/Components/{filename}", "r") as file:
        #             for line in file.readlines():
        #                 line_list.append(line)
        #                 print(f'{line}{" "*(len(line)-2)}|appended')
        #         with open(f"GAYM/{kre8dict['artributes'][3]}/{kre8dict['name']}/{filename[:-3]}.py", "w") as file:
        #             for line in line_list:
        #                 if line.find("kre8dict = {}") >= 0:
        #                     line = line.replace("kre8dict = {}", f"kre8dict = {kre8dict}")
        #                     print(line)
        #                 file.write(line)
        #                 print(f'{line}{" "*(len(line)-2)}|wrote')
        # os.mkdir(f"GAYM/{kre8dict['attributes'][3]}/{kre8dict['name']}/assets")
        self.create_spirite_sheet(img, kre8dict)
        return img

    # def create_spirite(self, kre8dict: dict, slot_pos=(0, 0)):
    #     """Create a game sprite using PNGs"""
    #     nim = Image.new('RGBA', (640, 640), (0, 0, 0, 0))
    #     print(slot_pos)
    #     # spirite_layers.append(addColor(random.choice(cl), fraim))
    #     for ltr in kre8dict["gaym"]:
    #         for nbr in range(4):
    #             fraim = stack_layers(kre8dict["gaym"][ltr][nbr], kre8dict["number_list"], kre8dict["color_list"])
    #             spirite_layers.append(fraim)
    #             print('gaymkre8dict' + str(kre8dict["gaym"][ltr][nbr]))
    #
    #     for layer in kre8dict["gaym"]:
    #         nim.paste(layer, (128, 128), mask=layer)
    #     # nim.paste(fraim, (0, 0), mask=fraim)
    #
    #     self.disp_img = ImageTk.PhotoImage(nim)
    #     kre8dict["Canvas"].create_image(slot_pos[0], slot_pos[1], image=self.disp_img)

    def stack_layers(self, spirite_choice: str, nl: list, colist: list, size: (int, int)) -> Image:
        """
        :return:
        """
        cl = []
        for color in colist:
            cl.append((int(color[0] * 255),
                       int(color[1] * 255),
                       int(color[2] * 255),
                       int(1.0 * 255)))
        obj_dict = gaym.GAYM_OBJECT_DICT[self.spirite_type_str_var.get()]
        layer_dict = LAYER_DICT[obj_dict[spirite_choice][0]]
        layers_list = list(layer_dict.keys())
        object_image = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
        if True:
            for layer in layers_list:
                pim = Image.open(f'assets/{obj_dict[spirite_choice][0]}/{layer}{random.choice(nl)}.png')
                cim = Image.new('RGBA', (128, 128), random.choice(cl))
                pim = pim.convert(mode='RGBA')
                cim = Image.blend(pim, cim, .55)
                object_image.paste(cim, (0, 0), mask=pim)
        return object_image.resize(size)


