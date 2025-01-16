import json
import random
import uu
# -*- coding: utf-8 -*-

"""
THE LOGIC FOR DISPLAYING ON KNIVOW.
"""

from PIL import Image, ImageDraw, ImageFont

from settings import *
ttf = ImageFont.truetype('emonob.ttf', 22)

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


def hangman(img: Image, kre8dict: dict) -> Image:
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    chosen_word = kre8dict["wordie"]["hangman"]["chosen"]
    hidden_word = kre8dict["wordie"]["hangman"]["hidden"]
    draw.multiline_text((w//2, h//6), text=HANGMAN_TEXTMAN_LIST[0], font=ttf)
    draw.text((w//2, int(h*(5/7))), text=dict_to_str(hidden_word), font=ttf)
    draw.text((w//8, h//6), text="Missed Letters:", font=ttf)
    return img


def update_hangman(img: Image, kre8dict: dict) -> Image:
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    chosen_word = kre8dict["wordie"]["hangman"]["chosen"]
    hidden_word = kre8dict["wordie"]["hangman"]["hidden"]
    missed_count = len(kre8dict["wordie"]["hangman"]["missed_letters"])
    draw.multiline_text((w//2, h//6), text=HANGMAN_TEXTMAN_LIST[missed_count], font=ttf)
    draw.text((w//2, int(h*(5/7))), text=dict_to_str(hidden_word), font=ttf)
    draw.text((w//8, h//6), text="Missed Letters:", font=ttf)
    draw.multiline_text((w//8, h//5), text=", ".join(kre8dict["wordie"]["hangman"]["missed_letters"]), font=ttf)
    return img


def dict_to_str(kre8dict: dict) -> str:
    hidden_word_dict = kre8dict
    hidden_word_str = ""
    for c in hidden_word_dict:
        hidden_word_str += hidden_word_dict[c]
    return hidden_word_str


def check_hangman_letter(letter_to_check: str, kre8dict: dict) -> dict:
    chosen_word = kre8dict["wordie"]["hangman"]["chosen"]
    hidden_word = kre8dict["wordie"]["hangman"]["hidden"]
    if letter_to_check in chosen_word:
        for i in range(len(chosen_word)):
            if letter_to_check*(i+1) in hidden_word:
                if hidden_word[letter_to_check*(i+1)] == " ◙ ":
                    hidden_word[letter_to_check*(i+1)] = f' {letter_to_check} '
    else:
        if letter_to_check in kre8dict["wordie"]["hangman"]["missed_letters"]:
            pass
        else:
            kre8dict["wordie"]["hangman"]["missed_letters"].append(letter_to_check)

    return hidden_word


def word_search(img: Image, kre8dict: dict) -> Image:
    """
    Create a 2d-array of letters with words in order.

    :param img:
    :param kre8dict:
    :return:
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    w, h = img.size
    letters_array = []
    word_list = ["KANISA", "BLUE"]
    font = ImageFont.truetype('trebucbd.ttf', 16)
    for i in range(nl[5]):
        word_picked = random.choice(list(kre8dict["word_dict"].keys()))
        word_list.append(word_picked.upper())
    for word in kre8dict["wordie"]:
        if word != "type" and word != "word_search":
            word_list.append(word.upper())
    kre8dict["wordie"]["word_search"]["word_list"] = word_list
    for x in range(0, w, 16):
        letters_array.append([])
        for y in range(0, h, 16):
            letters_array[x//16].append("")
    cx, cy = 0, 0
    for word in word_list:
        print(word)
        cx = random.randint(0, 16)
        orientation = random.choice(["Vertical", "Horizontal", "Diagonal"])
        if orientation == "Vertical":
            for c in word:
                print(cx, cy)
                letters_array[cx][cy] = c.upper()
                draw.text((cx*16+4, cy*16-2), font=font, text=c.upper(), fill=cl[1], align='right')
                cy += 1
        elif orientation == "Horizontal":
            for c in word:
                print(cx, cy)
                letters_array[cx][cy] = c.upper()
                draw.text((cx*16+4, cy*16-2), font=font, text=c.upper(), fill=cl[1], align='right')
                cx += 1
        elif orientation == "Diagonal":
            for c in word:
                print(cx, cy)
                letters_array[cx][cy] = c.upper()
                draw.text((cx*16+4, cy*16-2), font=font, text=c.upper(), fill=cl[1], align='right')
                cx += 1
                cy += 1
        # cy += 1

    # FILL IN THE REST OF SLOTS WITH RANDOM LETTERS.
    for cx in range(len(letters_array)):
        for cy in range(len(letters_array[cx])):
            if len(letters_array[cx][cy]) == 0:
                c = random.choice("abcdefghijklmnopqrstuvwxyz")
                letters_array[cx][cy] = c.upper()
                draw.text((cx*16+4, cy*16-2), font=font, text=c.upper(), fill=WHITE, align='right')
    # werd_serch_dict = {
    #     'letter_array': letters_array,
    #     'find_list': word_list
    # }
    kre8dict["wordie"]["word_search"]["letter_array"] = letters_array
    # with open(f'WORDIE/werd_serch_array.txt', 'w') as f:
    #     json.dump(werd_serch_dict, f, separators=(',', ': '))
    return img


def kollage(img: Image, kre8dict: dict) -> Image:
    """
    Create a collage of words on the img provided.
    """
    nl = kre8dict["number_list"]
    cl = kre8dict["color_list"]
    draw = ImageDraw.Draw(img)
    use_cl = []
    w, h = img.size
    for colo in cl:
        co0 = int(colo[0] * 255)
        co1 = int(colo[1] * 255)
        co2 = int(colo[2] * 255)
        use_cl.append((co0, co1, co2))
    for x in range(0, w, 64):
        for y in range(0, h, 32):
            rand_c = random.choice(kre8dict["use_id"])
            word = random.choice(ALPHANUMERIC_WORD_LISTS[rand_c])
            draw.text((x, y), text=word, fill=random.choice(use_cl), angle=random.randint(-nl[8], nl[8])*36)
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
