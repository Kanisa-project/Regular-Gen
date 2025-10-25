import os
import random
from tkinter import *
from PIL import Image, ImageDraw, ImageTk
from src.settings import app_settings

def load_spirite_layer(spirite_name: str, spirite_layer: str, layer_num: int) -> PhotoImage:
    file_path = f'{os.getcwd()[:-3]}/filesInput/spirites/{spirite_name}/{spirite_layer.lower()}{layer_num}.png'
    # print(f"Trying to load {file_path}")

    if not os.path.exists(file_path):
        # print(f"File not found: {file_path}")
        spirite_dir = f"{os.getcwd()[:-3]}/filesInput/spirites/{spirite_name}"
        if os.path.exists(spirite_dir):
            # print(f"Available files in directory:")
            for file in os.listdir(spirite_dir):
                print(f"  - {file}")
        else:
            print(f"Directory doesn't exist: {spirite_dir}")
        placeholder = PhotoImage(width=128, height=128)
        placeholder.put("#000000")
        return placeholder
    try:
        img = PhotoImage(file=file_path)
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        placeholder = PhotoImage(width=128, height=128)
        placeholder.put("#009900")
        return placeholder

def stack_layers(img: Image.Image, artribute_dict: dict, size=(128, 128)) -> Image.Image:
    """
    Stack the layers of a spirite with the options of the kre8shun dictionary.

    :param artribute_dict:
    :param img:
    :param kre8dict:
    :param size:
    :return:
    """
    object_str = artribute_dict['spirite']['spirite_type']
    cl = artribute_dict["colors"]
    object_image = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    print(artribute_dict['spirite'])
    for layer_dict in artribute_dict['spirite']['layers']:
        pim = Image.open(f'filesInput/spirites/{object_str}/{layer_dict["name"]}{layer_dict["number"]}.png')
        cim = Image.new('RGBA', (128, 128), random.choice(cl))
        pim = pim.convert(mode='RGBA')
        cim = Image.blend(pim, cim, artribute_dict['transparency'])
        object_image.paste(cim, (0, 0), mask=pim)
    return object_image.resize(size)


def add_foreground_bit(img: Image.Image, kre8dict: dict) -> Image.Image:
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


def add_color(color_to_add: tuple, image_to_color: Image) -> Image.Image:
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
