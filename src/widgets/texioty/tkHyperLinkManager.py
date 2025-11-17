# Sourced from effbot.org

from tkinter import *


class HyperlinkManager:

    def __init__(self, text):

        self.links = {}
        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.text.tag_config("command", foreground="yellow", underline=1)
        self.text.tag_bind("command", "<Enter>", self._enter)
        self.text.tag_bind("command", "<Leave>", self._leave)
        self.text.tag_bind("command", "<Button-1>", self._command_click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def add_cmd(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "command-%d" % len(self.links)
        self.links[tag] = action
        return "command", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return

    def _command_click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:8] == "command-":
                self.links[tag]()
                return
