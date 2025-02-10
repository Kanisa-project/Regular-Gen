import os
import random
from PIL import Image, ImageDraw, ImageFont
import settings as s

akt16 = ImageFont.truetype(os.getcwd() + "/assets/Fonts/Akt-Medium.ttf", 16)
akt32 = ImageFont.truetype(os.getcwd() + "/assets/Fonts/Akt-Medium.ttf", 32)


def add_ingredients(img: Image, kre8dict: dict) -> Image:
    ing_dict = kre8dict["recipe"]["ingredients"]
    draw = ImageDraw.Draw(img)
    width, height = img.size
    for i, (key, value) in enumerate(ing_dict.items()):
        x_position = 32 if i < 5 else 192 if i < 10 else 352
        y_position = (height * .15) + 5 * ((i % 5) * 3) if i < 10 else (height * .15) + 5 * (((i - 10) % 5) * 3)
        # y_position = (height * .1) + 5 * ((i % 5) * 3) if i < 10 else (height * .1) + 5 * (((i - 10) % 5) * 3)
        draw.text((x_position, y_position), text=f'{value[0]} {key}', font=akt16)
    return img


def add_directions(img: Image, kre8dict: dict) -> Image:
    dir_dict = kre8dict["recipe"]["directions"]
    draw = ImageDraw.Draw(img)
    width, height = img.size
    for i, (key, value) in enumerate(dir_dict.items()):
        draw.text((69, height * .275 + (10 * ((i * 2) + 2))),
                  text=f'{key}: {value}', font=akt16)
    return img


def add_labels(img: Image, kre8dict: dict) -> Image:
    """
    Stylize the titles for ingredients, directions, name, created by, and other information.
    :param img:
    :param kre8dict:
    :return:
    """
    draw = ImageDraw.Draw(img)
    width, height = img.size
    for _ in range(8):
        draw.text((16 + random.randint(-2, 2), (height * .1) + random.randint(-2, 2)),
                  text="  ".join("ingredients"), font=akt16,
                  fill=random.choice(s.RANDOM_COLORS))
        draw.multiline_text((16 + random.randint(-2, 2), (height * .275) + random.randint(-2, 2)),
                            text="\n".join("directions"), font=akt16,
                            fill=random.choice(s.RANDOM_COLORS))
        draw.text((width * .6 + random.randint(-2, 2), height * .8 + random.randint(-2, 2)),
                  text="created by: \n    -" + kre8dict["recipe"]["recipe_info"][0], font=akt16,
                  fill=random.choice(s.RANDOM_COLORS))
        draw.text((8 + random.randint(-2, 2), 4 + random.randint(-2, 2)),
                  text=kre8dict["recipe"]["recipe_info"][1], font=akt32,
                  fill=random.choice(s.RANDOM_COLORS))
    return img
