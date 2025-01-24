import random
from settings import *
from PIL import Image, ImageTk, ImageDraw


def resize_foto(foto: Image, new_size: tuple) -> Image:
    """Resize a foto and return it."""
    return foto.resize(new_size)


def crop_foto(foto: Image, cropping: (0, 0, 0, 0)) -> Image:
    """Crop a foto and return it."""
    return foto.crop(cropping)


def blend_foto(foto: Image, foto2: Image, blend_percent: float) -> Image:
    """Blend the two fotoes and return the one."""
    return Image.blend(foto, foto2, blend_percent)


def shuffle_foto(img: Image, kre8dict: dict) -> Image:
    """
    Slice and shuffle the provided image.

    :param img:
    :param kre8dict:
    :return:
    """
    crop_window_list = []
    sliced_images = []
    shuf_img_pos_list = []
    num_of_tiles = "4x4"
    if "Shuffle Size" in kre8dict:
        num_of_tiles = kre8dict["Shuffle Size"]
    w, h = img.size
    x_tiles = int(num_of_tiles.split("x")[0])
    y_tiles = int(num_of_tiles.split("x")[1])
    tile_xsize = w // x_tiles
    tile_ysize = h // y_tiles
    for x in range(0, w, tile_xsize):
        for y in range(0, h, tile_ysize):
            shuf_img_pos_list.append((x + 0, y + 0))
    for r in range(x_tiles):
        for c in range(y_tiles):
            x, y = c * tile_xsize, r * tile_ysize
            w, h = tile_xsize + x, tile_ysize + y
            crop_window_list.append((x, y, w, h))
            sliced_images.append(crop_foto(img, (x, y, w, h)))
    for simg in sliced_images:
        picked_pos = random.choice(shuf_img_pos_list)
        img.paste(simg, picked_pos)
        sdraw = ImageDraw.Draw(simg)
        sdraw.rectangle((0, 0, 13, 13), fill=BLACK)
        sdraw.text((0, 0), str(sliced_images.index(simg)))
        if sliced_images.index(simg) == len(sliced_images)-1:
            simg.paste(Image.new("RGB", (simg.size[0], simg.size[1]), color=DRS_PURPLE))
        simg.save(f".temp/{sliced_images.index(simg)}.png")
        shuf_img_pos_list.remove(picked_pos)
    return img


def hsb_filter_foto(img: Image, kre8dict: dict) -> Image:
    """
    Applies a hue, saturation, brightness filter to the provided image.

    :param img:
    :param kre8dict:
    :return:
    """
    hsb_im = img.convert('HSV')
    hsb_list = kre8dict["foto"]["HSB"]
    h, s, b = hsb_im.split()
    h = h.point(lambda p: p + hsb_list[0])
    s = s.point(lambda p: p * (hsb_list[1] // 10))
    b = b.point(lambda p: p * (hsb_list[2] // 10))
    img = Image.merge('HSV', (h, s, b))
    return img


def rgb_filter_foto(img: Image, kre8dict: dict) -> Image:
    """
    Applies a red, green, blue filter to the provided image.

    :param img: Image to be used in masterpiece.
    :param kre8dict: Dictionary with instructions on how to make masterpiece.
    :return:
    """
    rgb_im = img.convert('RGB')
    rgb_list = kre8dict["foto"]["RGB"]
    r, g, b = rgb_im.split()
    r = r.point(lambda p: p + rgb_list[0])
    g = g.point(lambda p: p + rgb_list[1])
    b = b.point(lambda p: p + rgb_list[2])
    img = Image.merge('RGB', (r, g, b))
    return img
