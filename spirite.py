import random
from tkinter import *
from PIL import Image, ImageDraw, ImageTk
from settings import *


def stack_layers(img: Image, kre8dict: dict, size=(128, 128)) -> Image:
    """
    Stack the layers of a spirite with the options of the kre8shun dictionary.

    :param img:
    :param kre8dict:
    :param size:
    :return:
    """
    print(kre8dict)
    object_str = list(kre8dict["spirite"].keys())[0]
    cl = []
    for color in kre8dict["color_list"]:
        cl.append((int(color[0] * 255),
                   int(color[1] * 255),
                   int(color[2] * 255),
                   int(1.0 * 255)))
    nl = kre8dict["number_list"]
    lnd = LAYER_DICT[object_str]
    layers_list = list(lnd.keys())
    object_image = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    for layer in layers_list:
        # pim = Image.open(f'assets/{object_str}/{layer}{random.choice(kre8dict["spirite"][object_str][layer])}.png')
        pim = Image.open(f'assets/{object_str}/{layer}{random.choice(nl)}.png')
        cim = Image.new('RGBA', (128, 128), random.choice(cl))
        pim = pim.convert(mode='RGBA')
        cim = Image.blend(pim, cim, .55)
        object_image.paste(cim, (0, 0), mask=pim)
    return object_image.resize(size)


def add_foreground_bit(img: Image, kre8dict: dict) -> Image:
    """
    Add different smaller images to give sparkly and other effects.
    :param img:
    :param kre8dict:
    :return:
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    fg_shape = random.choice(["bubble", "heart", "sparkle", "star0", "star1", "star2", "star3"])
    for i in range(nl[7]):
        pim = Image.open(f'assets/Foreground/{fg_shape}.png')
        rand_x, rand_y = (random.randint(nl[4], nl[7]), random.randint(nl[4], nl[7]))
        img.paste(pim, (rand_x * random.randint(4, 16), rand_y * random.randint(4, 16)), mask=pim)
    return img


def add_color(color_to_add: tuple, image_to_color: Image) -> Image:
    """
    Add color and transparency to an image.
    
    :param color_to_add: (0, 0, 0)
    :param image_to_color: Image
    :return:
    """
    int_color = (int(color_to_add[0] * 255), int(color_to_add[1] * 255), int(color_to_add[2] * 255), int(.32 * 255))
    im_overlay = Image.new(size=image_to_color.size, color=int_color, mode='RGBA')
    image_to_color.paste(im_overlay, None, mask=im_overlay)
    return image_to_color
