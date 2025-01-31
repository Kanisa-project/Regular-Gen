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

ttf = ImageFont.truetype(f'{os.getcwd()}/assets/Fonts/emonob.ttf', 22)

font_names = ["emono", "Parkinsans-Medium", "rogue", "Cookie-Regular", "berkshireswash-regular", "Akt-Medium",
              "AguafinaScript-Regular", "Charlie", "emonob", "fontello"]

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


def prompto(img: Image, kre8dict: dict) -> Image:
    """
    Creates a writing prompt from options within the Wordie tab.
    @param img:
    @param kre8dict:
    @return:
    """
    pass


def hangman(img: Image, artribute_dict: dict, option_dict: dict) -> Image:
    width_list = artribute_dict["accuracy"]
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    hidden_word = phrase_to_hidden_dict(option_dict["Phrase"])
    draw.multiline_text((w // 2, h // 6), text=HANGMAN_TEXTMAN_LIST[0], font=ttf, fill=random.choice(cl))
    draw.text((w // 2, int(h * (5 / 7))), text=dict_to_str(hidden_word), font=ttf, fill=random.choice(cl))
    draw.text((w // 8, h // 6), text="Missed Letters:", font=ttf, fill=random.choice(cl))
    return img


def update_hangman(img: Image, kre8dict: dict) -> Image:
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    chosen_word = kre8dict["wordie"]["hangman"]["chosen"]
    hidden_word = kre8dict["wordie"]["hangman"]["hidden"]
    missed_count = len(kre8dict["wordie"]["hangman"]["missed_letters"])
    draw.multiline_text((w // 2, h // 6), text=HANGMAN_TEXTMAN_LIST[missed_count], font=ttf)
    draw.text((w // 2, int(h * (5 / 7))), text=dict_to_str(hidden_word), font=ttf)
    draw.text((w // 8, h // 6), text="Missed Letters:", font=ttf)
    draw.multiline_text((w // 8, h // 5), text=", ".join(kre8dict["wordie"]["hangman"]["missed_letters"]), font=ttf)
    return img


def dict_to_str(kre8dict: dict) -> str:
    hidden_word_dict = kre8dict
    hidden_word_str = ""
    for c in hidden_word_dict:
        hidden_word_str += hidden_word_dict[c]
    return hidden_word_str


def phrase_to_hidden_dict(phrase: str) -> dict:
    hidden_phrase_dict = {}
    for c in phrase:
        if c in hidden_phrase_dict:
            c += c
        hidden_phrase_dict[c] = "◙"
    return hidden_phrase_dict


def check_hangman_letter(letter_to_check: str, kre8dict: dict) -> dict:
    chosen_word = kre8dict["wordie"]["hangman"]["chosen"]
    hidden_word = kre8dict["wordie"]["hangman"]["hidden"]
    if letter_to_check in chosen_word:
        for i in range(len(chosen_word)):
            if letter_to_check * (i + 1) in hidden_word:
                if hidden_word[letter_to_check * (i + 1)] == "◙":
                    hidden_word[letter_to_check * (i + 1)] = f' {letter_to_check} '
    else:
        if letter_to_check in kre8dict["wordie"]["hangman"]["missed_letters"]:
            pass
        else:
            kre8dict["wordie"]["hangman"]["missed_letters"].append(letter_to_check)

    return hidden_word


def word_search(img: Image, artribute_dict: dict, word_search_dict: dict) -> Image:
    """
    Create a 2d-array of letters with words in order.

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
    font = ImageFont.truetype('trebucbd.ttf', 16)
    for word in list(word_search_dict.values()):
        word_list.append(word.upper())
    # kre8dict["wordie"]["word_search"]["word_list"] = word_list
    for x in range(0, w, 16):
        letters_array.append([])
        for y in range(0, h, 16):
            letters_array[x // 16].append("")
    cx, cy = 0, 0
    for word in word_list:
        print(word)
        cx = random.randint(0, 16)
        orientation = random.choice(["Vertical", "Horizontal", "Diagonal"])
        if orientation == "Vertical":
            for c in word:
                print(cx, cy)
                letters_array[cx][cy] = c.upper()
                draw.text((cx * 16 + 4, cy * 16 - 2), font=font, text=c.upper(), fill=settings.QUARTZ, align='right')
                cy += 1
        elif orientation == "Horizontal":
            for c in word:
                print(cx, cy)
                letters_array[cx][cy] = c.upper()
                draw.text((cx * 16 + 4, cy * 16 - 2), font=font, text=c.upper(), fill=settings.QUARTZ, align='right')
                cx += 1
        elif orientation == "Diagonal":
            for c in word:
                print(cx, cy)
                letters_array[cx][cy] = c.upper()
                draw.text((cx * 16 + 4, cy * 16 - 2), font=font, text=c.upper(), fill=settings.QUARTZ, align='right')
                cx += 1
                cy += 1
        # cy += 1

    # FILL IN THE REST OF SLOTS WITH RANDOM LETTERS.
    for cx in range(len(letters_array)):
        for cy in range(len(letters_array[cx])):
            if len(letters_array[cx][cy]) == 0:
                c = random.choice("abcdefghijklmnopqrstuvwxyz")
                letters_array[cx][cy] = c.upper()
                draw.text((cx * 16 + 4, cy * 16 - 2), font=font, text=c.upper(), fill=random.choice(cl), align='right')
    # kre8dict["wordie"]["word_search"]["letter_array"] = letters_array
    return img


def kollage(img: Image, artribute_dict: dict, area_dict: dict) -> Image:
    """
    Create a collage of words on the img provided.
    """
    width_list = artribute_dict["accuracy"]
    cl = artribute_dict["colors"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    # draw.rectangle((0, 0, w, h), fill=random.choice(cl))
    font = random.choice(font_names)
    print(font)
    font = ImageFont.truetype(f'{os.getcwd()}/assets/Fonts/{font}.ttf', (random.choice(width_list) + 1) * 8)
    draw.text((random.randint(32, w - 256), random.randint(0, h // 8)), font=font, text=area_dict["Top"],
              fill=random.choice(cl))
    draw.text((random.randint(32, w - 256), random.randint((h * 7) // 8, h - 64)), font=font,
              text=area_dict["Bottom"],
              fill=random.choice(cl))
    draw.text((random.randint(w // 2, w), random.randint(0, h // 8)), font=font,
              text='\n'.join(area_dict["Right"]),
              fill=random.choice(cl))
    draw.text((random.randint(0, w // 2), random.randint(0, h // 8)), font=font,
              text='\n'.join(area_dict["Left"]),
              fill=random.choice(cl))
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


def riddler(img, artribute_dict, param):
    return None


def crossword(img, artribute_dict, param):
    return None
