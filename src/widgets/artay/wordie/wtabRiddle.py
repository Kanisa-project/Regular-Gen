from . import wordieTab


class Riddle(wordieTab.Wordietab):
    def __init__(self, width, height, master=None):
        super().__init__(width, height, master)
        self.setup_text_boxes({"Answer": "Sponge", "Clue 1": "Has holes", "Clue 2": "Holds water", "Clue 3": "What"}, width=32)

