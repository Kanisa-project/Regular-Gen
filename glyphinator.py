import random
from tkinter import *
from PIL import Image, ImageDraw, ImageTk
from settings import *


def snow_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    for w in range(64):
        for h in range(64):
            draw.point((w, h), fill=random.choice(color_list))
    return img


def whut_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    connection_point_list = [(0, 0), (.5, 0), (1, 0),
                             (0, .5), (.5, .5), (1, .5),
                             (0, 1), (.5, 1), (1, 1)]
    for i, colo in enumerate(color_list):
        con_pon = random.choice(connection_point_list)
        con_pon2 = random.choice(connection_point_list)
        x1 = con_pon[0] * w
        y1 = con_pon[1] * h
        x2 = con_pon2[0] * w
        y2 = con_pon2[1] * h
        # draw.line((x1, y1, x2, y2), width=3, fill=random.choice(color_list))
        draw.line((x1, y1, x2, y2), width=3, fill=colo)
    return img


def emoji_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    connection_point_list = [(0, 0), (.5, 0), (1, 0),
                             (0, .5), (.5, .5), (1, .5),
                             (0, 1), (.5, 1), (1, 1)]
    connection_path = [random.choice(connection_point_list)]
    for i in range(len(color_list)):
        connection_path.append(random.choice(connection_point_list))

    for i, colo in enumerate(color_list):
        con_pon = connection_path[i]
        con_pon2 = connection_path[i+1]
        next_con_pon = con_pon2
        x1 = con_pon[0] * w
        y1 = con_pon[1] * h
        x2 = next_con_pon[0] * w
        y2 = next_con_pon[1] * h
        draw.line((x1, y1, x2, y2), width=3, fill=colo)
    return img


def vertical_bity(img: Image, grey_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    for w in range(64):
        for h in range(64):
            draw.line((w, 0, w, h), fill=random.choice(grey_list))
    return img


# def generate_grey_list(tone_level=3) -> list:
#     """
#     Generate a list of grey colors.
#     @param tone_level: The number of greys that will appear.
#     @return:
#     """
#     greys = []
#     for t in range(tone_level):
#         grey_level = random.randint(1, 255//tone_level)
#         greys.append((grey_level*tone_level, grey_level*tone_level, grey_level*tone_level))
#     return greys


def horizontal_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    for w in range(64):
        for h in range(64):
            draw.line((0, h, w, h), fill=random.choice(color_list))
    return img


def spiral_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    for w in range(64):
        for h in range(64):
            draw.line((w, 64-h, 64-w, h), fill=random.choice(color_list))
    return img


def up_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w//2, h//2, (i+1)), 3, outline=random.choice(color_list))
    return img


def down_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w//2, h//2, (i+1)), 3, rotation=180, outline=random.choice(color_list))
    return img


def square_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(64):
        draw.regular_polygon((w//2, h//2, (i+1)), 4, outline=random.choice(color_list))
    return img


def plaid_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i, color in enumerate(color_list):
        draw.rectangle((0, 0, w, h), fill=random.choice(color_list))
    return img


def round_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(64):
        draw.regular_polygon((w//2, h//2, (i+1)), 8, outline=random.choice(color_list))
    return img


def ring_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(64):
        draw.circle((w//2, h//2), radius=64-i, fill=random.choice(color_list), outline=random.choice(color_list))
        # draw.ellipse(((w // 2, h // 2), (w, h)), fill=random.choice(color_list), outline=random.choice(color_list))
        # draw.ellipse(((w // 2, 0), (w, h // 2)), fill=random.choice(color_list), outline=random.choice(color_list))
        # draw.ellipse(((0, h*.75), (w*.25, h)), fill=random.choice(color_list), outline=random.choice(color_list))
    return img


def scales_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w//2, h//2, (96-i)), random.randint(3, 10), fill=random.choice(color_list), outline=random.choice(color_list))
    return img


# def scales_bity(img: Image, color_list: list) -> Image:
#     draw = ImageDraw.Draw(img)
#     w, h = (64, 64)
#     for i in range(96):
#         draw.regular_polygon((w//2, h//2, (96-i)), random.randint(3, 10), rotation=270, outline=random.choice(color_list))
#     return img


# def greytone_gridder(img: Image, kre8dict: dict) -> Image:
#     """
#     Create a grid style frame of grey tone .png files for Kinvow.
#     :param kre8dict: KrE8shun dictionary.
#     :param img:
#     :return:
#     """
#     print(kre8dict)
#     # greytoneImage = Image.new('RGBA', (640, 640), (100, 0, 10, 0))
#     new_img = img
#     number_lists = []
#     tone = list(kre8dict["Glyph"].keys())[0]
#     shape_list = kre8dict["Glyph"][tone]
#     nl = kre8dict["number_list"]
#     cl = kre8dict["color_list"]
#     for w in range(10):
#         number_lists.append([])
#         for h in range(10):
#             # ZIGZAG THE GLYPH BITS
#             if w % 2 == 0:
#                 if h % 2 == 0:
#                     number_lists[w].append(nl[0])
#                 else:
#                     number_lists[w].append(nl[1])
#             else:
#                 if h % 2 == 0:
#                     number_lists[w].append(nl[1])
#                 else:
#                     number_lists[w].append(nl[0])
#
#             if tone == "None":
#                 fn = f'assets/Avatar/Mandel{random.choice(nl)}.png'
#                 ttim = Image.open(fn)
#             else:
#                 fn = f'assets/{tone}/{random.choice(shape_list)}{random.choice(nl)}.png'
#                 ttim = Image.open(fn)
#             new_img.paste(ttim, (w * 64, h * 64))
#             # greytoneImage.paste(ttim, (w * 64, h * 64))
#     return new_img


# def addColor(color_to_add: tuple, image_to_color: Image) -> Image:
#     """Add some color to an image."""
#     print(color_to_add)
#     int_color = (int(color_to_add[0] * 255), int(color_to_add[1] * 255), int(color_to_add[2] * 255), int(.5 * 255))
#     im_overlay = Image.new(size=image_to_color.size, color=int_color, mode='RGBA')
#     image_to_color.paste(im_overlay, None, mask=im_overlay)
#     return image_to_color


def slant_up_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(-4, 72):
        draw.line((0, i, 64, i-4), fill=random.choice(color_list))
    return img


def slant_down_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(-4, 72):
        draw.line((0, i, 64, i+4), fill=random.choice(color_list))
    return img


def slant_left_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(-4, 72):
        draw.line((i, 0, i-4, 64), fill=random.choice(color_list))
    return img


def slant_right_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for i in range(-4, 72):
        draw.line((i, 0, i+4, 64), fill=random.choice(color_list))
    return img


def left_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w//2, h//2, (i+1)), 3, rotation=90, outline=random.choice(color_list))
    return img


def right_bity(img: Image, color_list: list) -> Image:
    draw = ImageDraw.Draw(img)
    w, h = (64, 64)
    for i in range(96):
        draw.regular_polygon((w//2, h//2, (i+1)), 3, rotation=270, outline=random.choice(color_list))
    return img
