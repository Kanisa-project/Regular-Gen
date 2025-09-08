from dataclasses import dataclass
from typing import Any
import tkinter as tk


@dataclass
class Kre8Dict:
    use_id="R4nd0M"
    use_utc="0123654789"

@dataclass
class TexiotyProfile:
    username: str
    password: str
    color_theme: tuple


@dataclass
class DisplayComponent:
    """
    Display some text as a label widget or edit some text as an entry widget.
    """
    default_value: str
    var: tk.StringVar = None
    label_widget: tk.Widget = None
    new_entry_widget: tk.Widget = None
    edit_entry_widget: tk.Widget = None

    def set_var(self, new_var: str):
        """
        Set the StringVar of this display component.
        :param new_var: String of info.
        :return:
        """
        self.var.set(new_var)


@dataclass
class Command:
    name: str
    handler: Any
    help_message: str
    possible_args: dict
    helper_type: str
    text_color: str
    bg_color: str

@dataclass
class EventDataCard:
    eventType: DisplayComponent
    eventDate: DisplayComponent
    eventTime: DisplayComponent
    eventCreator: DisplayComponent
    eventCreatedUTC: DisplayComponent
    info_categories = ["event_type", "event_date", "event_time", "event_creator", "event_created_utc"]
