import random
from ...features.artay import meemcap

from PIL import Image
from pathlib import Path
from src.domain.resource_loader import asset_path

from . import artstyle

SENSES = ["see", "pick up", "eat", "sniff", "hear", "reach for"]
PHYS_OBJ = ["t-shirt", "glove", "apple", "egg", "cricket", "bag", "slug", "eraser"]
COMPL = ["dripping", "spinning", "wrapped", "covered", "rolling", "squeezing", "dancing", "baked"]
EMENT = ["honey", "newspaper", "napkin", "coffee", "pebbles"]
QUANTITY = ["a", "some", "about"]


class Meem(artstyle.Artyle):
    def __init__(self, width, height, master=None):
        super(Meem, self).__init__(master=master, width=width, height=height)
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
        og_memes_dir = Path(asset_path("OG_Memes"))
        candidates = [p for p in og_memes_dir.iterdir()
                      if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".gif")]
        if not candidates:
            raise FileNotFoundError(f"No memes found in {og_memes_dir}")
        meme_path = random.choice(candidates)
        meme_imaj = Image.open(meme_path)

        paste_xy = (int(img.size[0] * 0.420), int(img.size[1] * 0.420))
        if "A" in meme_imaj.getbands():
            img.paste(meme_imaj, paste_xy, mask=meme_imaj)
        else:
            img.paste(meme_imaj, paste_xy)
        meemcap.add_caps_meem(img, artributes, kre8dict["meem"]['da_fuq'])
        return img

    def generate_top_bottom(self):
        rand_sense = random.choice(SENSES)
        rand_obj = random.choice(PHYS_OBJ)
        rand_compl = random.choice(COMPL)
        rand_ement = random.choice(EMENT)
        rand_quant = random.choice(QUANTITY)
        comp_subj = "it's"
        if rand_quant == "a" and rand_obj[0] in ['a', 'e', 'i', 'o', 'u']:
            rand_quant += "n"
        if rand_quant == "some":
            rand_obj += 's'
            comp_subj = "they"
        if rand_quant == "about":
            rand_quant += f" {random.randint(0, 14)}"
            comp_subj = "they"
            rand_obj += 's'
        rand_top = f"When you {rand_sense} {rand_quant} {rand_obj}"
        rand_bot = f"{random.choice(['but', 'and'])} {comp_subj} {rand_compl} in {rand_ement}"
        self.textbox_dict["Top"][0].set(rand_top)
        self.textbox_dict["Bottom"][0].set(rand_bot)
