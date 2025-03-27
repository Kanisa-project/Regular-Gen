from p5 import *

from settings import *
import random


def new_color_list(id_used: str, is_float=True) -> list:
    """
    Create a new color list with the given ID string.

    :param id_used: ID string being used to create the color list.
    :param is_float: If the tuple is created with Floats or Integers.
    :return: list
    """
    color_list = []
    for c in id_used:
        if c.lower() in ALPHANUMERIC_COLORS:
            kolor = ALPHANUMERIC_COLORS[c.lower()]
        else:
            kolor = PUNCTUATION_COLORS[c.lower()]
        if is_float:
            kolor = (round(kolor[0] / 255, 3),
                     round(kolor[1] / 255, 3),
                     round(kolor[2] / 255, 3))

        color_list.append(kolor)
    return color_list


def setup():
    size(420, 420)
    no_fill()
    global cl
    cl = new_color_list("pringles", False)


def draw():
    for p in polypointlist(3, 0, mouse_x, mouse_y, 75):
        for p2 in polypointlist(6, 0, p[0], p[1], 20):
            stroke(random.randint(0, 155), random.randint(0, 155), random.randint(155, 255))
            stroke_weight(random.randint(1, 10))
            stroke_weight(3)
            ellipse(p2[0], p2[1], 40, 40)

def run_p5():
    run()
