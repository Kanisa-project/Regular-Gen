import random
import wordieTab


class WordSearch(wordieTab.Wordietab):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.word_value_list = ["Zero", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]

        self.setup_button_choices(["Random Words"])
        self.button_dict["Random Words"][1].config(command=self.randomize_words)
        self.setup_labels(["Words to find: "], start_x_cell=1)
        self.setup_number_wheel("num_boxes", self.update_number_of_text_boxes, start_y_cell=1)
        # self.setup_dropdown_menus(word_list=list(range(0, 10)),
        #                           start_x_cell=0, start_y_cell=1, dropdown_name="num_boxes")

    def delete_word_boxes(self):
        for textbox in list(self.textbox_dict.keys()):
            self.textbox_dict[textbox][1].destroy()

    def update_number_of_text_boxes(self, num_boxes: int):
        self.delete_word_boxes()
        boxes = {}
        for i in range(num_boxes):
            boxes[str(i)] = self.word_value_list[i + 1]
        if boxes in self.widget_display_array:
            self.widget_display_array.remove(boxes)
        self.setup_text_boxes(boxes, start_x_cell=2)

    def randomize_words(self):
        for textbox in list(self.textbox_dict.keys()):
            self.textbox_dict[textbox][0].set(random.choice(self.word_value_list))
