import math
import random
import tkinter as tk
import settings as s

import idutc


class artributalCanvas(tk.Canvas):
    def __init__(self, width=32, height=32, master=None, start_emoji="🐫"):
        super(artributalCanvas, self).__init__(master=master, width=width, height=height,
                                               bg=s.rgb_to_hex(s.DIM_GREY + tuple([0])))

        self.artribute_title = "Size"
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.dragone)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.emoji_rep = self.create_text(16, 16, text=start_emoji, font=("Times New Roman", 20))
        self.isSelected = False
        self.master = master
        self.start_x = 0
        self.start_y = 0

    def start_drag(self, event):
        self.isSelected = True
        self.start_x = self.winfo_pointerx() - self.winfo_x()
        self.start_y = self.winfo_pointery() - self.winfo_y()
        # print(self.isSelected)

    def dragone(self, event):
        if self.isSelected:
            mouse_x = self.winfo_pointerx()
            mouse_y = self.winfo_pointery()
            new_x = mouse_x - self.start_x
            new_y = mouse_y - self.start_y
            self.place(x=new_x,
                       y=new_y)

    def stop_drag(self, event):
        self.isSelected = False

    def update_artribute_emoji(self, keeword: str) -> str:
        emoji_text = ""
        # print(keeword)
        if "Door" in keeword:
            self.itemconfig(self.emoji_rep, text="🚪")
            # emoji_text = "🚪"
        elif "Window" in keeword:
            self.itemconfig(self.emoji_rep, text="🪟")
            # emoji_text = "🪟"
        elif "Cloud" in keeword:
            self.itemconfig(self.emoji_rep, text="☁️")
            # emoji_text = "☁️"
        elif "Rainbow" in keeword:
            self.itemconfig(self.emoji_rep, text="🌈")
            # emoji_text = "🌈"
        elif "Fire" in keeword:
            self.itemconfig(self.emoji_rep, text="🔥")
            # emoji_text = "🔥"
        elif "Ice" in keeword:
            self.itemconfig(self.emoji_rep, text="🧊")
            # emoji_text = "🧊"
        elif "Camel" in keeword:
            self.itemconfig(self.emoji_rep, text="🐫")
            # emoji_text = "🐫"
        elif "Chicken" in keeword:
            self.itemconfig(self.emoji_rep, text="🐓")
            # emoji_text = "🐓"
        elif "Dog" in keeword:
            self.itemconfig(self.emoji_rep, text="🐶")
            # emoji_text = "🐶"
        elif "Rock" in keeword:
            self.itemconfig(self.emoji_rep, text="🗿")
            # emoji_text = "🗿"
        elif "Sock" in keeword:
            self.itemconfig(self.emoji_rep, text="🧦")
            # emoji_text = "🧦"
        elif "Crayon" in keeword:
            self.itemconfig(self.emoji_rep, text="🖍️")
            # emoji_text = "🖍️"
        elif "Pen" in keeword:
            self.itemconfig(self.emoji_rep, text="🖋")
            # emoji_text = "🖋"
        return emoji_text
