import random

import wordieTab
import settings as s

PHRASE_LIST = ["You gave Sally a cheese wheel, she buried it under a tree.",
               "You helped Tom move a couch, he burned it on the porch.",
               "Shane kicked your shin after you gave him a flower.",
               "This is just a phrase, we'll go out of it soon."]

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


class Hangman(wordieTab.Wordietab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(["Random Phrase"])
        self.button_dict["Random Phrase"][1].config(command=self.randomize_phrase)
        self.setup_text_boxes({"Phrase": random.choice(PHRASE_LIST)}, start_x_cell=1, width=42)
        self.setup_number_wheel("max_guesses", self.call_this_back)
        self.max_guesses = 0

        self.gaim_phrase = self.textbox_dict["Phrase"][0].get()

    def call_this_back(self, extra):
        self.max_guesses = extra

    def randomize_phrase(self):
        self.textbox_dict["Phrase"][0].set(random.choice(PHRASE_LIST))


def check_hangman_letter(letter_to_check: str) -> dict:
    chosen_word = self.gaim_phrase
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
