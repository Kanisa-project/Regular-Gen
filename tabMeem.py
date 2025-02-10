import os
import random
import meemcap

from PIL import Image

import artstyle

SENSES = ["see", "pick up", "eat", "sniff", "hear", "reach for"]
PHYS_OBJ = ["t-shirt", "glove", "apple", "egg", "cricket", "mouse"]
COMPL = ["dripping", "spinning", "wrapped", "covered", "rolling", "squeezing"]
EMENT = ["honey", "newspaper", "cinnamon bark", "coffee", "pebbles"]
QUANTITY = ["a", "some"]


class Meem(artstyle.Artyle):
    def __init__(self, width, height, master=None, idutc=None):
        super(Meem, self).__init__(master=master, idutc=idutc, width=width, height=height)
        self.setup_button_choices(["MixUp"])
        self.setup_radiobutton_choices(["da_fuq", "forever_alone", "LLOOOLL", "me_gusta", "mother_of_god",
                                        "oh_kay", "srsly", "troll_face"], start_x_cell=1)
        self.setup_text_boxes({"Top": "When you see a beach ball",
                               "Bottom": "and it's covered in ants"}, width=32, start_x_cell=3)
        self.button_dict["MixUp"][1].config(command=self.generate_top_bottom)

    def gather_meem_options(self) -> dict:
        chosen_meem_options = {
            "Image Name": self.radiobutton_dict["da_fuq"][0].get()
        }
        if self.radiobutton_dict["da_fuq"][0].get() == 0:
            chosen_meem_options["da_fuq"] = {}
            for i, word in enumerate(self.textbox_dict):
                chosen_meem_options["da_fuq"][word] = self.textbox_dict[word][0].get()
        return chosen_meem_options

    def add_meem(self, img: Image, kre8dict: dict, abt="masterpiece") -> Image:
        artributes = self.set_artributes(kre8dict)
        meme_imaj = Image.open(
            os.getcwd() + '\\assets\\OG_Memes\\' + random.choice(os.listdir(os.getcwd() + '\\assets\\OG_Memes')))
        img.paste(meme_imaj, (int(img.size[0] * .420), int(img.size[1] * .420)))
        meemcap.add_caps_meem(img, artributes, kre8dict['meem']['da_fuq'])
        return img

    def generate_top_bottom(self):
        rand_sense = random.choice(SENSES)
        rand_obj = random.choice(PHYS_OBJ)
        rand_compl = random.choice(COMPL)
        rand_ement = random.choice(EMENT)
        rand_quant = random.choice(QUANTITY)
        comp_subj = "it"
        if rand_quant == "a" and rand_obj[0] in ['a', 'e', 'i', 'o', 'u']:
            rand_quant += "n"
        if rand_quant == "some":
            rand_obj += 's'
            comp_subj = "they"
        rand_top = f"When you {rand_sense} {rand_quant} {rand_obj}"
        rand_bot = f"{random.choice(['but', 'and'])} {comp_subj} started {rand_compl} in {rand_ement}"
        self.textbox_dict["Top"][0].set(rand_top)
        self.textbox_dict["Bottom"][0].set(rand_bot)
