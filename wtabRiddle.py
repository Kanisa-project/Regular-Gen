import wordieTab


class Riddle(wordieTab.Wordietab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.setup_text_boxes({"Answer": [], "Clue 1": [], "Clue 2": []})
