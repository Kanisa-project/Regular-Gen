from tkinter import StringVar, IntVar, Label, Scale, Entry, OptionMenu, Radiobutton, Button, Checkbutton
from typing import List
from tkinter import ttk

from src.widgets.texioty import Texioty
from src.widgets.texioty.helpers.tex_helper import TexiotyHelper


class BasikWidget(TexiotyHelper, ttk.LabelFrame):
    def __init__(self, width, height, master=None, text="Basic"):
        """
        Base widget with some basic functions for setting up any other widget.
        :param width:
        :param height:
        :param master:
        """
        if master and isinstance(master, Texioty):
            ttk.LabelFrame.__init__(self, master=None, width=width, height=height)
            TexiotyHelper.__init__(self, txo=master.texoty, txi=master.texity)
        else:
            ttk.LabelFrame.__init__(self, master=master, width=width, height=height)
            print("No texioty detexted")
            print(type(master))
        self.tab_name = "Basic"
        self.grid_propagate(False)

        self.font = ("Helvetica", int(width * 0.02))

        self.checkbutton_dict = {}
        self.radiobutton_dict = {}
        self.button_dict = {}
        self.textline_dict = {}
        self.textbox_dict = {}
        self.slider_dict = {}
        self.slider_limit_dict = {}
        self.dropdown_menu_dict = {}
        self.listbox_dict = {}

        self.widget_display_array = []
        self.helper_commands = {}

    def update_slider_label(self) -> str:
        return str(self.widget_display_array)

    def setup_slider_bars(self, slider_list: list, start_x_cell=0, start_y_cell=0, slide_len=88):
        """
        Set up a dictionary of sliders for a given list of parameters. Used in conjunction with slider_limit_dict.

        :param slide_len:
        :param start_y_cell:
        :param start_x_cell:
        :param slider_list: A list of parameter names.
        """
        self.widget_display_array.append(slider_list)

        def _snap_to_click(event, s: Scale):
            width = max(1, s.winfo_width())
            frac = max(0.0, min(1.0, event.x / width))
            v_from = float(s['from'])
            v_to = float(s['to'])
            value = v_from + frac * (v_to - v_from)
            res = float(s['resolution'])
            if res > 0:
                value = round(value / res) * res
            s.set(value)
            return 'break'

        for i, parameter in enumerate(slider_list):
            min_val, max_val = self.slider_limit_dict[parameter]
            str_var = StringVar(value=parameter + " : ")
            int_var = IntVar(value=(max_val + min_val) // 2)
            label = Label(self, textvariable=str_var, font=self.font)
            scale = Scale(self, from_=min_val, to=max_val, variable=int_var, width=12, length=slide_len,
                          orient="horizontal", borderwidth=0, sliderlength=22, showvalue=True,
                          command=lambda e: self.update_slider_label())
            scale.bind("<Button-3>", lambda e, s = scale: _snap_to_click(e, s))
            self.slider_dict[parameter] = [int_var, str_var, scale, label]

            row = i % 8
            col = i // 10
            scale.grid(column=start_x_cell + col+1, row=row + start_y_cell, sticky="e", columnspan=1)
            label.grid(column=start_x_cell + col, row=row + start_y_cell, sticky="w")

    def setup_dropdown_menus(self, word_list: list, dropdown_name="", start_x_cell=0, start_y_cell=0):
        """
        Create some dropdown menus based off a list of words or a single word.
        :param start_y_cell:
        :param start_x_cell:
        :param word_list: List of words to include in the dropdown menu.
        :param dropdown_name: Name this dropdown menu.
        :return:
        """
        self.widget_display_array.append(dropdown_name)
        word_str_var = StringVar(value=word_list[0])
        self.dropdown_menu_dict[dropdown_name] = [word_str_var,
                                                  OptionMenu(self, word_str_var, *word_list)]
        self.dropdown_menu_dict[dropdown_name][1].grid(column=start_x_cell, row=start_y_cell)

    def setup_radiobutton_choices(self, options_list: list, start_x_cell=0, start_y_cell=0):
        """
        Radio buttons are part of the same choices, only one of the options can be selected at a time.
        :param start_y_cell:
        :param start_x_cell:
        :param options_list: list of options for the radio buttons
        :return: None
        """
        # Create the variable to keep track of chosen decision and add the options to display in the Artyle frame.
        int_var = IntVar()
        self.widget_display_array.append(options_list)
        # Build each button with the same int_var to keep track correctly.
        for i, option in enumerate(options_list):
            new_str_var = StringVar(value=option)
            radiobutton = Radiobutton(self, text=option, variable=int_var, value=i, font=self.font)
            row = (i % 10)
            col = (i // 10)
            radiobutton.grid(column=col + start_x_cell, row=row + start_y_cell)
            self.radiobutton_dict[option] = [int_var, new_str_var, radiobutton]

    def setup_text_boxes(self, keyed_dict: dict, start_x_cell=0, start_y_cell=0, width=10):
        """
        Set up a specified number of text boxes on the artyle tab.

        :param keyed_dict:
        :param width:
        :param start_y_cell:
        :param start_x_cell:
        """
        for i, word in enumerate(keyed_dict):
            lbl_str = StringVar(value=word + ": ")
            lbl = Label(self, textvariable=lbl_str)
            str_var = StringVar(value=keyed_dict[word])
            entry = Entry(self, textvariable=str_var, width=width)
            self.textbox_dict[word] = [str_var, entry]
            row = (i % 5)
            col = (i // 5)
            lbl.grid(column=col + start_x_cell, row=row + start_y_cell, sticky='e')
            entry.grid(column=col + start_x_cell + 1, row=row + start_y_cell, stick='w')

    def setup_button_choices(self, button_list: List[str], start_x_cell=0, start_y_cell=0):
        """
        Take in a list of texts and create a button for each one, starting at the specified cell.

        :param start_x_cell: Starting column for the buttons.
        :param start_y_cell: Starting row for the buttons.
        :param button_list: List of words for buttons to use.
        :return:
        """
        self.widget_display_array.append(button_list)
        for i, option in enumerate(button_list):
            str_var = StringVar(value=option)
            button = Button(self, textvariable=str_var, font=self.font)
            self.button_dict[option] = [str_var, button]

            row = (i % 8)
            col = (i // 8)

            button.grid(column=start_x_cell + col, row=start_y_cell + row)

    def setup_checkbutton_choices(self, word_list: List[str], start_x_cell=0, start_y_cell=0):
        """
        Take in a list of words and create a checkbutton for each one, starting at the specified cell.

        :param start_x_cell: Starting column for the check buttons.
        :param start_y_cell: Starting row for the check buttons.
        :param word_list: A list of words to be used as options.
        """
        self.widget_display_array.append(word_list)
        for i, option in enumerate(word_list):
            int_var = IntVar()
            str_var = StringVar(value=option)
            checkbutton = Checkbutton(self, text=option, variable=int_var, font=self.font)

            self.checkbutton_dict[option] = [int_var, str_var, checkbutton]

            row = (i % 10)
            col = (i // 10)

            checkbutton.grid(column=col+start_x_cell, row=row+start_y_cell)
