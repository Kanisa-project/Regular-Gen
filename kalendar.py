import tkinter as tk
import calendar
import datetime

import helper_widget
import settings as s
import texoty

day_abbrv = ["S", "M", "T", "W", "Th", "F", "Sa"]
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
years = ["2022", "2023", "2024", "2025", "2026", "2027"]


class Kalendar(helper_widget.helpingWidget):
    """ Keeps track of dates and events."""
    def __init__(self, width, height, master=None):
        super(Kalendar, self).__init__(master=master, width=width, height=height, text="Calendar:  ")
        self.dbh = None
        self.txo: texoty.TEXOTY = None
        self.width = width
        self.height = height
        self.month_num = datetime.date.today().month
        self.year_num = datetime.date.today().year
        self.cal = calendar.Calendar(6)
        self.grid_propagate(False)
        self.selected_month_var = tk.StringVar()
        # self.selected_month_var.set("May")
        # self.selected_month_var.set("February")
        self.selected_year_var = tk.StringVar()
        # self.selected_year_var.set("2024")
        # self.selected_year_var.set("2025")
        self.setup_dropdown_menus(word_list=months, dropdown_name="DropMonths", start_x_cell=2)
        self.setup_dropdown_menus(word_list=years, dropdown_name="DropYears", start_x_cell=5)
        self.setup_button_choices(["<<"], start_x_cell=1)
        self.setup_button_choices([">>"], start_x_cell=3)
        self.button_dict["<<"][1].config(command=self.prev_month_btn_press)
        self.button_dict[">>"][1].config(command=self.next_month_btn_press)
        for d in day_abbrv:
            day_lbl = tk.Label(self, text=d)
            day_lbl.grid(row=1, column=day_abbrv.index(d) + 1)
        self.month_cal = self.cal.monthdayscalendar(2024, 1)
        self.day_btn_list = []
        self.create_day_buttons(self.selected_month_var.get())
        self.texioty_commands = {
            "new_event": [self.create_cal_event, "Create a new event in the calalander.",
                          {}, "CLDR", s.rgb_to_hex(s.LIGHT_STEEL_BLUE), s.rgb_to_hex(s.DARK_SLATE_BLUE)]
        }

    def destroy_day_buttons(self):
        for btn in self.day_btn_list:
            btn.destroy()

    def create_day_buttons(self, args):
        self.destroy_day_buttons()
        ri = 1
        ci = 0
        self.month_cal = self.cal.monthdayscalendar(self.year_num, self.month_num)
        for week in self.month_cal:
            ri += 1
            for day in week:
                ci += 1
                day_btn = tk.Button(self, width=int(self.width // 60), height=int(self.height // 180),
                                    text=day if day != 0 else '-',
                                    command=lambda: self.txo.priont_list(self.month_cal, "[]"),
                                    bg=s.rgb_to_hex(
                                        s.LIGHT_SLATE_BLUE) if day == datetime.date.today().day else s.rgb_to_hex(
                                        s.BEIGE))
                day_btn.grid(row=ri, column=ci, sticky='news', pady=2, padx=2)
                if ci > 6:
                    ci = 0
                self.day_btn_list.append(day_btn)

    # def update_month_selected(self, args):
    #     print(datetime.date.today().month)
    #     print(months[datetime.date.today().month])

    def prev_month_btn_press(self):
        self.month_num -= 1
        self.selected_month_var.set(months[self.month_num-1])
        self.create_day_buttons('')

    def next_month_btn_press(self):
        self.month_num += 1
        self.selected_month_var.set(months[self.month_num-1])
        self.create_day_buttons('')

    # def create_event_buttons(self, event_list: list):
    #     for item in event_list:
    #         eve_btn = tk.Button(self, text=item)
    #         eve_btn.grid(column=1, row=event_list.index(item)+9, columnspan=2)

    def create_cal_event(self, args):
        self.txo.master.start_question_prompt({
            "event_type": ["What type of event it this?", "", "Birthday"]
        })
