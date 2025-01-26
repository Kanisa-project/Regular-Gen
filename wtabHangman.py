import wordieTab


class Hangman(wordieTab.Wordietab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_button_choices(["Random Phrase"])
        self.setup_labels(["Phrase: ", "Max Missed Guess: "], start_x_cell=1)
        # self.setup_text_boxes(["This is just a phrase, we'll go out of it soon."], start_x_cell=1, width=42)
        self.setup_dropdown_menus(word_list=list(range(0, 10)),
                                  start_x_cell=2, start_y_cell=1, dropdown_name="max_missed")
