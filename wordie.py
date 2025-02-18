import json
import random
import uu
import os

import settings

# -*- coding: utf-8 -*-

"""
THE LOGIC FOR DISPLAYING ON KNIVOW.
"""

from PIL import Image, ImageDraw, ImageFont

from settings import *


FONT_NAME = "Akt-Medium"
mono_font_names = ["CodygoonRegular-oweO0", "trebucbd.ttf"]
font_names = ["Parkinsans-Medium", "rogue", "Cookie-Regular", "berkshireswash-regular",
              "Akt-Medium", "AguafinaScript-Regular", "Charlie", "fontello", "CodygoonRegular-oweO0",
              "Gisshiri-4nLDD", "SuboleyaRegular-qZeV1",
              "Jemgonzademo-lgRqw", "Stars-DEa1", "MintsodaLimeGreen13X16Regular-KVvzA", "PixgamerRegular-OVD6A"]

HANGMAN_TEXTMAN_LIST = ["  ╔═════╕   \n"
                        "  ║     ┇   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔═════╕   \n"
                        "  ║     ┇   \n"
                        "  ║     ◯   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔═════╕   \n"
                        "  ║     ┇   \n"
                        "  ║     ◯   \n"
                        "  ║     ‡   \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔═════╕   \n"
                        "  ║     ┇   \n"
                        "  ║     ◯   \n"
                        "  ║    /‡   \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔═════╕   \n"
                        "  ║     ┇   \n"
                        "  ║     ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔═════╕   \n"
                        "  ║     ┇   \n"
                        "  ║     ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║    /    \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔═════╕   \n"
                        "  ║     ┇   \n"
                        "  ║     ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║    / \\ \n"
                        "  ║         \n"
                        "══╩═════════\n"
                        ]


def hangman(img: Image, artribute_dict: dict, option_dict: dict) -> Image:
    width_list = artribute_dict["accuracy"]
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    font = FONT_NAME
    # print(font)
    font = ImageFont.truetype(f'{os.getcwd()}/assets/Fonts/{font}.ttf', (random.choice(width_list) + 1) * 8)
    hidden_word = phrase_to_hidden_dict(option_dict["Phrase"])
    draw.multiline_text((w // 2, h // 6), text=HANGMAN_TEXTMAN_LIST[0], font=font, fill=random.choice(cl))
    draw.text((w // 2, int(h * (5 / 7))), text=dict_to_str(hidden_word), font=font, fill=random.choice(cl))
    draw.text((w // 8, h // 6), text="Missed Letters:", font=font, fill=random.choice(cl))
    return img


def dict_to_str(hidden_word_dict: dict) -> str:
    """
    Converts a hidden phrase dictionary into a regular string.
    :param hidden_word_dict: Phrase to be extrapolated from.
    :return:
    """
    hidden_word_str = ""
    for c in hidden_word_dict:
        hidden_word_str += hidden_word_dict[c]
    return hidden_word_str


def phrase_to_hidden_dict(phrase: str) -> dict:
    """
    Converts a phrase into a hidden dictionary used for phrase guessing gaims.
    :param phrase:
    :return:
    """
    hidden_phrase_dict = {}
    for c in phrase:
        if c in hidden_phrase_dict:
            c += c
        if c not in "abcdefghijklmnopqrstuvwxyz":
            hidden_phrase_dict[c] = c[0]
        else:
            hidden_phrase_dict[c] = "◙"
    return hidden_phrase_dict


def word_search(img: Image, artribute_dict: dict, word_search_dict: dict) -> Image:
    """
    Create a 2d-array of letters with words in gridded fashion.

    :param word_search_dict:
    :param artribute_dict:
    :param img:
    :return:
    """
    width_list = artribute_dict["accuracy"]
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    letters_array = []
    word_list = []
    font = ImageFont.truetype(random.choice(mono_font_names), (random.choice(width_list)*2) % 16)
    for word in list(word_search_dict.values()):
        word_list.append(word.upper())
    for x in range(0, w, 16):
        letters_array.append([])
        for y in range(0, h, 16):
            letters_array[x // 16].append("")
    cx, cy = 0, 0
    for word in word_list:
        cx = random.randint(0, 16)
        orientation = random.choice(["Vertical", "Horizontal", "Diagonal"])
        if orientation == "Vertical":
            for c in word:
                letters_array[cx][cy] = c.upper()
                draw.text((cx * 16 + 4, cy * 16 - 2), font=font, text=c.upper(), fill=settings.QUARTZ, align='right')
                cy += 1
        elif orientation == "Horizontal":
            for c in word:
                letters_array[cx][cy] = c.upper()
                draw.text((cx * 16 + 4, cy * 16 - 2), font=font, text=c.upper(), fill=settings.QUARTZ, align='right')
                cx += 1
        elif orientation == "Diagonal":
            for c in word:
                letters_array[cx][cy] = c.upper()
                draw.text((cx * 16 + 4, cy * 16 - 2), font=font, text=c.upper(), fill=settings.QUARTZ, align='right')
                cx += 1
                cy += 1

    # FILL IN THE REST OF SLOTS WITH RANDOM LETTERS.
    for cx in range(len(letters_array)):
        for cy in range(len(letters_array[cx])):
            if len(letters_array[cx][cy]) == 0:
                c = random.choice("abcdefghijklmnopqrstuvwxyz")
                letters_array[cx][cy] = c.upper()
                draw.text((cx * 16 + 4, cy * 16 - 2), font=font, text=c.upper(), fill=random.choice(cl), align='right')
    return img


def kollage(img: Image, artribute_dict: dict, area_dict: dict) -> Image:
    """
    Create a collage of words on the img provided.
    """
    width_list = artribute_dict["accuracy"]
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    font = FONT_NAME
    print(font)
    font = ImageFont.truetype(f'{os.getcwd()}/assets/Fonts/{font}.ttf', 16)
    draw.text((w * 0.5, h * 0.125), anchor=random.choice(["rs", "la"]), font=font, text=area_dict["Top"], fill=random.choice(cl))
    draw.text((w * 0.5, h * 0.875), anchor=random.choice(["lt", "rb"]), font=font, text=area_dict["Bottom"], fill=random.choice(cl))
    draw.text((w * 0.875, h * 0.125), font=font, text='\n'.join(area_dict["Right"]), fill=random.choice(cl))
    draw.text((w * 0.125, h * 0.125), font=font, text='\n'.join(area_dict["Left"]), fill=random.choice(cl))
    # draw.text((random.randint(32, w - 256), random.randint(0, h // 8)), font=font, text=area_dict["Top"],
    #           fill=random.choice(cl))
    # draw.text((random.randint(32, w - 256), random.randint((h * 7) // 8, h - 64)), font=font,
    #           text=area_dict["Bottom"],
    #           fill=random.choice(cl))
    # draw.text((random.randint(w // 2, w), random.randint(0, h // 8)), font=font,
    #           text='\n'.join(area_dict["Right"]),
    #           fill=random.choice(cl))
    # draw.text((random.randint(0, w // 2), random.randint(0, h // 8)), font=font,
    #           text='\n'.join(area_dict["Left"]),
    #           fill=random.choice(cl))
    return img


def poetree(img: Image, kre8dict: dict) -> Image:
    """
    Creates a poem that rhymes and stuff.
    @param img:
    @param kre8dict:
    @return:
    """
    pass


def lyrix(img: Image, kre8dict: dict) -> Image:
    """
    Gather lyrics from the internets.
    """
    pass


def digiary(img: Image, kre8dict: dict) -> Image:
    """
    Create a masterpiece from a digiary entry. Or create a digiary entry.
    """
    pass


def riddler(img, artribute_dict, riddle_dict: dict) -> Image:
    width_list = artribute_dict["accuracy"]
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # draw.rectangle((0, 0, w, h), fill=random.choice(cl))
    font = random.choice(font_names)
    print(font)
    clue_1_str = "I " + riddle_dict['Clue 1'].lower() + ","
    clue_2_str = "I still " + riddle_dict['Clue 2'].lower() + ","
    clue_3_str = riddle_dict['Clue 3']
    answer_str = riddle_dict["Answer"]
    font = ImageFont.truetype(f'{os.getcwd()}/assets/Fonts/{font}.ttf', (random.choice(width_list) + 1) * 8)
    draw.text((w * .333, h * .2), font=font, text=clue_1_str,
              fill=random.choice(cl))
    draw.text((w * .333, h * .4), font=font, text=clue_2_str,
              fill=random.choice(cl))
    draw.text((w * .333, h * .6), font=font, text=clue_3_str,
              fill=random.choice(cl))
    draw.text((w * .333, h * .8), font=font, text=answer_str,
              fill=random.choice(cl))
    return img


def crossword(img, artribute_dict, crossed_dict: dict) -> Image:
    width_list = artribute_dict["accuracy"]
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # draw.rectangle((0, 0, w, h), fill=random.choice(cl))
    font = random.choice(font_names)
    font = ImageFont.truetype(f'{os.getcwd()}/assets/Fonts/{font}.ttf', (random.choice(width_list) + 1) * 8)
    spec_char = "◘" * 6
    spec_char2 = "◘".join(["\n", "\n", "\n", "\n", "\n", "\n", "\n"])
    draw.text((w * .333, h * .2), font=font, text=spec_char,
              fill=random.choice(cl))
    draw.text((w * .333, h * .2), font=font, text=spec_char2,
              fill=random.choice(cl))
    return img
