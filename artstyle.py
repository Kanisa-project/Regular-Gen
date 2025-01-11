from tkinter import *
from settings import *
from tkinter import ttk


class Artyle(ttk.Frame):
    def __init__(self, width, height, master=None, idutc=None, texioty=None):
        """
        Base art style tab that has buttons, sliders, checkboxes and dropdown menus for choosing options from within
        a glyth, glyph, wordie, sprite, gaym, mujic, foto and any other forms of art style.

        :param width:
        :param height:
        :param master:
        :param idutc:
        :param texioty:
        """
        super(Artyle, self).__init__(master=master, width=width, height=height)
        self.TEXIOTY = texioty
        self.IDUTC_frame: idutc.IDUTC = idutc
        self.tab_name = "Basic"
        self.checkbutton_dict = {}
        self.radiobutton_dict = {}
        self.textbox_dict = {}
        self.slider_dict = {}
        self.slider_limit_dict = {}
        self.button_dict = {}
        self.optionmenu_dict = {}
        self.dropdown_menu_dict = {}
        self.chosen_options_dict = {}

        # List of widget names for displaying inside the Artyle frame.
        self.widget_display_array = []

    def update_slider_label(self) -> str:
        return str(self.widget_display_array)

    def setup_slider_bars(self, slider_list: list):
        """
        Set up a dictionary of sliders for a given list of parameters. Used in conjunction with slider_limit_dict.

        :param slider_list: A list of parameter names.
        """
        self.widget_display_array.append(slider_list)
        for i, parameter in enumerate(slider_list):
            min_val, max_val = self.slider_limit_dict[parameter]
            str_var = StringVar(value=parameter + " : ")
            int_var = IntVar(value=(max_val + min_val) // 2)
            label = Label(self, textvariable=str_var)
            scale = Scale(self, from_=min_val, to=max_val, variable=int_var, width=5, length=88,
                          orient="horizontal", borderwidth=0, sliderlength=6, showvalue=False,
                          command=lambda: self.update_slider_label())
            self.slider_dict[parameter] = [int_var, str_var, scale, label]

            row = i % 8
            col = i // 10
            scale.grid(column=len(self.widget_display_array) + col, row=row, sticky="se")
            label.grid(column=len(self.widget_display_array), row=row, sticky="nw")

    def setup_dropdown_menus(self, word_list=None, word_str=None, dropdown_name=""):
        """
        Create some dropdown menus based off a list of words or a single word.
        :param word_list: List of words to include in the dropdown menu.
        :param word_str: A string to get random words for the dropdown menu.
        :param dropdown_name: Name this dropdown menu.
        :return:
        """
        # If it is a single string, collect random words for the dropdown menu
        if word_str:
            self.widget_display_array.append(word_str)
            for c in word_str:
                while c in self.dropdown_menu_dict:
                    c += c
                words_str_var = StringVar(value=ALPHANUMERIC_WORD_LISTS[c[:1].lower()][0])
                self.dropdown_menu_dict[c] = [words_str_var,
                                              OptionMenu(self, words_str_var, *ALPHANUMERIC_WORD_LISTS[c[:1].lower()])]
        # If it's a list, just add the list of words to the dropdown menu.
        elif word_list:
            self.widget_display_array.append(dropdown_name)
            word_str_var = StringVar(value=word_list[0])
            self.dropdown_menu_dict[dropdown_name] = [word_str_var,
                                                      OptionMenu(self, word_str_var, *word_list)]
        # Add each dropdown menu to the artyle frame.
        for i, dropdown in enumerate(list(self.dropdown_menu_dict.keys())):
            row = i % 10
            col = i // 10
            self.dropdown_menu_dict[dropdown][1].grid(column=len(self.widget_display_array) + col, row=row)

    def setup_radiobutton_choices(self, options_list: list):
        """
        Radio buttons are part of the same choices, only one of the options can be selected at a time.
        :param options_list: list of options for the radio buttons
        :return: None
        """
        # Create the variable to keep track of chosen decision and add the options to display in the Artyle frame.
        int_var = IntVar()
        self.widget_display_array.append(options_list)
        # Build each button with the same int_var to keep track correctly.
        for i, option in enumerate(options_list):
            new_str_var = StringVar(value=option)
            radiobutton = Radiobutton(self, text=option, variable=int_var, value=i)
            radiobutton.grid(column=len(self.widget_display_array) + 0, row=i)
            self.radiobutton_dict[option] = [int_var, new_str_var, radiobutton]

    def setup_text_boxes(self, many: int):
        """
        Set up a specified number of text boxes in the artyle tab.

        :param many: The number of text boxes to set up.
        """
        self.widget_display_array.append([])
        for i, _ in enumerate(range(many)):
            str_var = StringVar(value="4x4")
            entry = Entry(self, textvariable=str_var)
            key = f"{i}"
            self.textbox_dict[key] = [str_var, entry]

            row = (i % 5 + 1)
            col = (i // 5 + 1)

            entry.grid(column=col + len(self.widget_display_array), row=row)

    def setup_button_choices(self, button_list: list):
        """
        Set up buttons on the artyle tab.

        :param button_list: List of words for buttons to use.
        :return:
        """
        self.widget_display_array.append(button_list)
        for i, option in enumerate(button_list):
            str_var = StringVar(value=option)
            button = Button(self, textvariable=str_var)
            self.button_dict[option] = [str_var, button]

            row = (i % 8)
            col = (i // 8)

            button.grid(column=len(self.widget_display_array) + col, row=row)

    def setup_checkbutton_choices(self, word_list: list):
        """
        Set up checkbutton choices on the artyle tab.

        :param word_list: A list of words to be used as options.
        """
        self.widget_display_array.append(word_list)
        for i, option in enumerate(word_list):
            int_var = IntVar()
            str_var = StringVar(value=option)
            checkbutton = Checkbutton(self, text=option, variable=int_var)

            self.checkbutton_dict[option] = [int_var, str_var, checkbutton]

            row = (i % 8)
            col = (i // 8)

            checkbutton.grid(column=len(self.widget_display_array)+col, row=row)
