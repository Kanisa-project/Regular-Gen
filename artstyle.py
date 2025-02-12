from tkinter import *
from settings import *
from tkinter import ttk


class Artyle(ttk.Frame):
    def __init__(self, width, height, master=None, idutc=None, texioty=None):
        """
        Base art style tab that has buttons, sliders, checkboxes and dropdown menus for choosing options from within
        a glyth, glyph, wordie, sprite, gaim, mujic, foto and any other forms of art style.

        :param width:
        :param height:
        :param master:
        :param idutc:
        :param texioty:
        """
        super(Artyle, self).__init__(master=master, width=width, height=height)
        # self.TEXIOTY = texioty
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
                          orient="horizontal", borderwidth=0, sliderlength=6, showvalue=True,
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
            radiobutton = Radiobutton(self, text=option, variable=int_var, value=i)
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
            col = (i // 5 + 1)
            lbl.grid(column=col + start_x_cell - 1, row=row + start_y_cell, sticky='e')
            entry.grid(column=col + start_x_cell, row=row + start_y_cell, columnspan=2)

    def setup_button_choices(self, button_list: list, start_x_cell=0, start_y_cell=0):
        """
        Set up buttons on the artyle tab.

        :param start_y_cell:
        :param start_x_cell:
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

            button.grid(column=start_x_cell + col, row=start_y_cell + row)

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

            row = (i % 10)
            col = (i // 10)

            checkbutton.grid(column=len(self.widget_display_array) + col, row=row)

    def set_artributes(self, kre8dict: dict) -> dict:
        selected_colors = []
        artribute_dict = {}

        if kre8dict["artributes"][1] == "Door":
            artribute_dict["transparency"] = 0.85
        elif kre8dict["artributes"][1] == "Window":
            artribute_dict["transparency"] = 0.35

        if kre8dict["artributes"][2] == "Rainbow":
            for ltr in kre8dict["use_id"]:
                if ltr.lower() in ALPHANUMERIC_COLORS:
                    selected_colors.append(ALPHANUMERIC_COLORS[ltr.lower()])
                else:
                    selected_colors.append(PUNCTUATION_COLORS[ltr.lower()])
        elif kre8dict["artributes"][2] == "Cloud":
            shadelvl = 255 // len(kre8dict["use_id"])
            for i in range(len(kre8dict["use_id"])):
                selected_colors.append(((i + 1) * shadelvl, (i + 1) * shadelvl, (i + 1) * shadelvl))
        artribute_dict['colors'] = selected_colors

        if kre8dict["artributes"][4] == "Chicken":
            artribute_dict['size_scale'] = 0.2
        elif kre8dict["artributes"][4] == "Dog":
            artribute_dict['size_scale'] = 0.4
        elif kre8dict["artributes"][4] == "Camel":
            artribute_dict['size_scale'] = 0.8

        if kre8dict["artributes"][6] == "Pen":
            artribute_dict["accuracy"] = kre8dict["number_list"][:3]
        elif kre8dict["artributes"][6] == "Crayon":
            artribute_dict["accuracy"] = kre8dict["number_list"][3:]

        return artribute_dict
