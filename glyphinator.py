import random
from tkinter import *
from PIL import Image, ImageDraw, ImageTk

import settings
from settings import *


def snow_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    for w in range(64):
        for h in range(64):
            draw.point((w, h), fill=random.choice(cl))
    return img


def spiral_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    for w in range(64):
        for h in range(64):
            draw.line((w, 64 - h, 64 - w, h), fill=random.choice(cl))
    return img


def whut_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    connection_point_list = [(0, 0), (1, 0), (0, 1), (1, 1)]
    draw.rectangle((0, 0, w, h), fill=random.choice(cl))
    if random.randint(0, 100) % 2 == 0:
        for point in connection_point_list:
            con_pon = point
            con_pon2 = (.5, .5)
            x1 = con_pon[0] * w
            y1 = con_pon[1] * h
            x2 = con_pon2[0] * w
            y2 = con_pon2[1] * h
            draw.line((x1, y1, x2, y2), width=3, fill=cl[0])
            # draw.line((x1, y1, x2, y2), width=3, fill=random.choice(cl))
            # draw.line((x1, y1, x2, y2), width=3, fill=colo)
    else:
        draw.ellipse(((0, 0), (w, h)), width=3, outline=cl[0])
    return img


def emoji_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    connection_point_list = [(0, 0), (.5, 0), (1, 0),
                             (0, .5), (.5, .5), (1, .5),
                             (0, 1), (.5, 1), (1, 1)]
    connection_path = [random.choice(connection_point_list)]
    for i in range(len(cl)):
        connection_path.append(random.choice(connection_point_list))
    draw.rectangle((0, 0, w, h), fill=random.choice(cl))
    for i, colo in enumerate(cl):
        con_pon = connection_path[i]
        con_pon2 = connection_path[i + 1]
        next_con_pon = con_pon2
        x1 = con_pon[0] * w
        y1 = con_pon[1] * h
        x2 = next_con_pon[0] * w
        y2 = next_con_pon[1] * h
        draw.line((x1, y1, x2, y2), width=3, fill=colo)
    return img


def vertical_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    for w in range(64):
        for h in range(64):
            draw.line((w, 0, w, h), fill=random.choice(cl))
    return img


def horizontal_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    for w in range(64):
        for h in range(64):
            draw.line((0, h, w, h), fill=random.choice(cl))
    return img


def slant_up_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(-4, 72):
        draw.line((0, i, w, i - 4), fill=random.choice(cl))
    return img


def slant_down_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(-4, 72):
        draw.line((0, i, w, i + 4), fill=random.choice(cl))
    return img


def slant_left_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(-4, 72):
        draw.line((i, 0, i - 4, h), fill=random.choice(cl))
    return img


def slant_right_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(-4, 72):
        draw.line((i, 0, i + 4, h), fill=random.choice(cl))
    return img


def left_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w // 2, h // 2, (i + 1)), 3, rotation=90, outline=random.choice(cl))
    return img


def right_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w // 2, h // 2, (i + 1)), 3, rotation=270, outline=random.choice(cl))
    return img


def up_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w // 2, h // 2, (i + 1)), 3, outline=random.choice(cl))
    return img


def down_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w // 2, h // 2, (i + 1)), 3, rotation=180, outline=random.choice(cl))
    return img


def square_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(64):
        draw.regular_polygon((w // 2, h // 2, (i + 1)), 4, outline=random.choice(cl))
    return img


def plaid_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    draw.rectangle((0, 0, w, h), fill=random.choice(cl))
    # draw.rectangle((0, 0, w, h), fill=random.choice(cl) + tuple([50]))
    return img


def round_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    draw.rectangle((0, 0, w, h), fill=random.choice(cl))
    for i in range(36):
        draw.regular_polygon((w // 2, h // 2, (i + 1)), 8, outline=random.choice(cl))
    return img


def ring_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    draw.rectangle((0, 0, w, h), fill=random.choice(cl))
    for i in range(32):
        draw.ellipse(((i, i), (w-i, h-i)), fill=random.choice(cl), outline=random.choice(cl))
    return img


def scales_bity(img: Image, artribute_dict: dict) -> Image:
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w // 2, h // 2, (96 - i)), random.randint(3, 10), fill=random.choice(cl),
                             outline=random.choice(cl))
    return img
