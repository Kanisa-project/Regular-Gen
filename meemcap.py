from PIL import Image, ImageDraw, ImageFont
from settings import *


font_names = ["Parkinsans-Medium", "Akt-Medium", "emonob", "fontello"]


def add_caps_meem(img: Image, artribute_dict: dict, area_dict: dict) -> Image:
    """
    Create a collage of words on the img provided.
    """
    width_list = artribute_dict["accuracy"]
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # draw.rectangle((0, 0, w, h), fill=random.choice(cl))
    font = random.choice(font_names)
    font = ImageFont.truetype(f'{os.getcwd()}/assets/Fonts/{font}.ttf', 32)
    draw.text((64, h * .33), font=font, text=area_dict["Top"],
              fill=random.choice(cl))
    draw.text((64, h * .66), font=font,
              text=area_dict["Bottom"],
              fill=random.choice(cl))
    return img
