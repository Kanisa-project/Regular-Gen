import random

import wordieTab
import settings as s

PHRASE_LIST = ["You gave Sally a cheese wheel, she buried it under a tree.",
               "You helped Tom move a couch, he burned it on the porch.",
               "Shane kicked your shin after you gave him a flower.",
               "This is just a phrase, we'll go out of it soon."]

HANGMAN_TEXTMAN_LIST = ["  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱        \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤════╕   \n"
                        "  ║╱╱    ┇   \n"
                        "  ║╱     ◯   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║     ‡   \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║    /‡   \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║         \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║    /    \n"
                        "  ║         \n"
                        "══╩═════════\n",

                        "  ╔╤╤═══╕   \n"
                        "  ║╱╱   ┇   \n"
                        "  ║╱    ◯   \n"
                        "  ║    /‡\\ \n"
                        "  ║     ‡   \n"
                        "  ║    / \\ \n"
                        "  ║         \n"
                        "══╩═════════\n"
                        ]
missed_letters = []
gaim_phrase = "This is one two."
max_guesses = 0


class Hangman(wordieTab.Wordietab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(["Random Phrase"])
        self.button_dict["Random Phrase"][1].config(command=self.randomize_phrase)
        self.setup_text_boxes({"Phrase": random.choice(PHRASE_LIST)}, start_x_cell=1, width=42)
        self.setup_number_wheel("max_guesses", self.call_this_back, start_y_cell=1)
        self.max_guesses = 0

        self.gaim_phrase = self.textbox_dict["Phrase"][0].get()

    def call_this_back(self, extra):
        self.max_guesses = extra
        # set_local_max(extra)

    def randomize_phrase(self):
        self.textbox_dict["Phrase"][0].set(random.choice(PHRASE_LIST))


# def set_local_max(new_maxNone):
#     max_guesses += new_max


def check_hangman_letter(letter_to_check: str, hidden_dict: dict) -> dict:
    print(hidden_dict)
    if letter_to_check in gaim_phrase:
        for i in range(len(gaim_phrase)):
            if letter_to_check * (i + 1) in hidden_dict:
                if hidden_dict[letter_to_check * (i + 1)] == "◙":
                    hidden_dict[letter_to_check * (i + 1)] = letter_to_check
    else:
        if letter_to_check in missed_letters:
            pass
        else:
            missed_letters.append(letter_to_check)
    # if len(missed_letters) >= max_guesses:
    #     missed_letters.clear()
    return hidden_dict
