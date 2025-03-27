import random
import tkinter as tk
import calendar
import datetime
from dataclasses import dataclass
from typing import Dict

import helper_widget
# import dummyHelper
import settings as s
import questionnairePrompts as Qp
# import lisox

# import dbhelper
# import texoty

day_abbrv = ["S", "M", "T", "W", "Th", "F", "Sa"]
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
month_abbrv = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
years = ["2021", "2022", "2023", "2024", "2025", "2026", "2027"]


@dataclass
class EventDataCard:
    eventType: s.DisplayComponent
    eventDate: s.DisplayComponent
    eventTime: s.DisplayComponent
    eventCreator: s.DisplayComponent
    eventCreatedUTC: s.DisplayComponent

    info_categories = ["event_type", "event_date", "event_time", "event_creator", "event_created_utc"]


@dataclass
class CalendarEventIndex:
    calendar_events: Dict[str, EventDataCard]

    def add_calendar_event(self, args):
        print("calendar event index args: ", args)
        if isinstance(args, dict):
            new_dated_event = args
        else:
            new_dated_event = dummyHelper.generate_dummy_calendar_event()
        self.calendar_events[new_dated_event['event_date']] = EventDataCard(
            eventType=new_dated_event['event_type'],
            eventDate=new_dated_event['event_date'],
            eventTime=new_dated_event['event_time'],
            eventCreator=new_dated_event['event_creator'],
            eventCreatedUTC=new_dated_event['event_created_utc']
        )
        print(new_dated_event)


class Kalendar(helper_widget.helpingWidget):
    """ Keeps track of dates and events."""

    def __init__(self, width, height, master=None):
        super(Kalendar, self).__init__(master=master, width=width, height=height, text="Calendar:  ")
        self.dbh = None
        self.txo = None
        self.width = width
        self.height = height
        self.todays_date = f'{datetime.date.today().year}-{months[datetime.date.today().month-1]}-{datetime.date.today().day}'
        self.month_num = datetime.date.today().month
        self.year_num = datetime.date.today().year
        self.cal = calendar.Calendar(6)
        self.selected_day_button = None
        self.grid_propagate(False)
        self.selected_month_var = tk.StringVar()
        self.selected_month_var.set(months[self.month_num - 1])
        self.selected_year_var = tk.StringVar()
        self.selected_year_var.set(str(self.year_num))
        self.month_dropdown = tk.OptionMenu(self, self.selected_month_var, *months, command=self.create_day_buttons)
        self.month_dropdown.grid(row=0, column=1, columnspan=3)
        self.year_dropdown = tk.OptionMenu(self, self.selected_year_var, *years, command=self.create_day_buttons)
        self.year_dropdown.grid(row=0, column=5, columnspan=3)
        self.previous_month_btn = tk.Button(self, text='<<', command=self.prev_month_btn_press)
        self.previous_month_btn.grid(column=1, rowspan=1, row=0)
        self.next_month_btn = tk.Button(self, text='>>', command=self.next_month_btn_press)
        self.next_month_btn.grid(column=3, rowspan=1, row=0)
        for d in day_abbrv:
            day_lbl = tk.Label(self, text=d)
            day_lbl.grid(row=1, column=day_abbrv.index(d) + 1)
        self.month_cal = self.cal.monthdayscalendar(int(self.selected_year_var.get()), 1)
        self.day_btn_list = []
        self.create_day_buttons([])
        self.texioty_commands = {}

    def destroy_day_buttons(self):
        for btn in self.day_btn_list:
            btn.destroy()

    def create_day_buttons(self, args):
        """Create a DayButton for each day of the month."""
        self.destroy_day_buttons()
        ri = 0
        column_index = 0
        self.month_cal = self.cal.monthdayscalendar(int(self.selected_year_var.get()),
                                                    months.index(self.selected_month_var.get())+1)
        for week in self.month_cal:
            ri += 1
            for day in week:
                column_index += 1
                day_btn = DayButton(master=self, width=int(self.width // 60), height=int(self.height // 180),
                                    text=day if day != 0 else '-',
                                    fixed_ri=ri - 1, fixed_ci=column_index - 1)
                day_btn.grid(row=ri, column=column_index, sticky='news', pady=2, padx=2)
                if day_btn.isDateToday:
                    self.selected_day_button = day_btn
                if column_index > 6:
                    column_index = 0
                self.day_btn_list.append(day_btn)

    def print_clicked_date(self, day: str):
        date_stamp = f"{self.selected_year_var.get()}-{month_abbrv[self.month_num - 1]}-{day}"
        self.txo.master.texity.command_string_var.set(date_stamp)

    def prev_month_btn_press(self):
        if self.month_num == 1:
            self.month_num = 12
            self.year_num -= 1
            self.selected_year_var.set(str(self.year_num))
        else:
            self.month_num -= 1
        self.month_num = s.clamp(self.month_num, 1, 12)
        self.selected_month_var.set(months[self.month_num - 1])
        self.create_day_buttons([])
        for day_btn in self.day_btn_list:
            if day_btn.day == "1":
                self.selected_day_button = day_btn
                continue

    def next_month_btn_press(self):
        if self.month_num == 12:
            self.month_num = 1
            self.year_num += 1
            self.selected_year_var.set(str(self.year_num))
        else:
            self.month_num += 1
        self.selected_month_var.set(months[self.month_num-1])
        self.create_day_buttons([])
        for day_btn in self.day_btn_list:
            if day_btn.day == "1":
                self.selected_day_button = day_btn
                continue


class DayButton(tk.Button):
    """A button customized for adding or removing events per each day. Stylized based on the logged in profile."""

    def __init__(self, width=None, height=None, text=None, command=None, bg=None,
                 master: Kalendar=None, fixed_ri=None, fixed_ci=None):
        super().__init__(master, width=width, height=height, text=text, command=self.day_button_clicked,
                         bg=bg)
        self.master = master
        self.row_index = fixed_ri
        self.column_index = fixed_ci
        self.day = f'{master.month_cal[self.row_index][self.column_index]}'
        self.date = f'{master.selected_year_var.get()}-{master.selected_month_var.get()}-{self.day}'
        self.bind("<Button-3>", self.right_click_submenu)
        self.isDisabled = False
        self.isSelected = False
        self.isDateToday = False
        todays_date = f'{datetime.date.today().year}-{months[datetime.date.today().month-1]}-{datetime.date.today().day}'
        if self.date == todays_date:
            self.isDateToday = True
        if self.day == '0':
            self.isDisabled = True
            self.config(state='disabled')
        self.set_background_color()

    def right_click_submenu(self, event):
        """Bring up the submenu from right-clicking."""
        if not self.isDisabled:
            submenu = tk.Menu(self, tearoff=0)
            submenu.add_command(label="New Event",
                                command=self.add_new_event)
            submenu.add_command(label="Delete Event",
                                command=self.delete_event)
            submenu.tk_popup(event.x_root, event.y_root)

    def add_new_event(self):
        """Add a new event to the kalendar."""
        self.master.txo.priont_string(f"Add a new event on {self.date}.")

    def delete_event(self):
        """Delete an event that was cancelled."""
        self.master.txo.priont_string(f"Delete an event from {self.date}.")

    def day_button_clicked(self):
        """Whenever a day button is clicked, make it the new selection."""
        self.isSelected = not self.isSelected
        if self.isSelected:
            self.master.selected_day_button.day_button_clicked()
            self.master.selected_day_button = self
            self.master.txo.priont_string(f"{self.date} date selected.")
        self.set_background_color()

    def deselect_previous_day_button(self, prev_btn):
        pass

    # def select_new_day_button(self, new_btn):
    #     if isinstance(self.master.selected_day_button, DayButton):
    #         self.master.selected_day_button.day_button_clicked()
    #     else:
    #         self.master.selected_day_button = self

    def set_background_color(self):
        """Set the background color of the button based on different possible states."""
        if self.isSelected:
            self.config(bg=s.rgb_to_hex(s.LIGHT_SEA_GREEN))
        elif self.isDateToday:
            self.config(bg=s.rgb_to_hex(s.LIGHT_SLATE_BLUE))
        elif self.isDisabled:
            self.config(bg=s.rgb_to_hex(s.LIGHT_GREY))
        else:
            self.config(bg=s.rgb_to_hex(s.BEIGE))
