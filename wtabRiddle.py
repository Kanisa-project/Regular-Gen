import wordieTab


class Riddle(wordieTab.Wordietab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_text_boxes({"Answer": "Sponge", "Clue 1": "Has holes", "Clue 2": "Holds water"}, width=32)
