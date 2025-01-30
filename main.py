import artay
# import helperIMX
# import helperPIN
import idutc
# import helperLRC
import tkinter as tk
import settings as s
import texioty
import kinvow
import subprocess
import threading
import kalendar
import gaimPlay

large_widgets = ["Texioty", "Kinvow"]
small_widgets = ["Calendar", "IDUTC", "Artay"]


def start_simple_client():
    client_script_path = "./test_client.py"
    threading.Thread(target=subprocess.run, args=(["python", client_script_path], )).start()


class Application(tk.Frame):
    def __init__(self, screen_w: int, screen_h: int, master=None):
        """
        Primary application window with all the widgets required.
        :param master:
        """
        super().__init__(master)
        self.idutc_frame = idutc.IDUTC(width=screen_w*.333, height=screen_h*.4)

        self.artay_frame = artay.ARTAY(width=screen_w*.333, height=screen_h*.4, idutc_frame=self.idutc_frame)

        self.texioty_frame = texioty.TEXIOTY(width=screen_w//3, height=screen_h*.93)

        self.kinvow_frame = kinvow.KINVOW(width=screen_w//3, height=screen_h*.93,
                                          idutc_frame=self.idutc_frame, artay_frame=self.artay_frame)
        self.kinvow_frame.txo = self.texioty_frame.texoty

        self.calendar_frame = kalendar.Kalendar(width=screen_w*.333, height=screen_h*.4)
        self.calendar_frame.txo = self.texioty_frame.texoty

        self.gaimplay_frame = gaimPlay.gaimPlayer(width=screen_w*.333, height=screen_h*.4)
        self.gaimplay_frame.txo = self.texioty_frame.texoty

        self.texioty_frame.add_helper_widget("CLDR", self.calendar_frame)
        self.texioty_frame.add_helper_widget("IDUT", self.idutc_frame)
        self.texioty_frame.add_helper_widget("KNVO", self.kinvow_frame)
        self.texioty_frame.add_helper_widget("ARTY", self.artay_frame)
        self.texioty_frame.add_helper_widget("PLAY", self.gaimplay_frame)

        self.widget_dict = {
            "Texioty": self.texioty_frame,
            "Calendar": self.calendar_frame,
            "IDUTC": self.idutc_frame,
            "Kinvow": self.kinvow_frame,
            "Artay": self.artay_frame,
            "gaimPlay": self.gaimplay_frame
        }
        self.center_frame = SpotLighter(widget_dict=self.widget_dict, width=screen_w//3, height=screen_h//4)
        self.center_frame.grid(column=1, row=1, columnspan=1, rowspan=1, padx=1, pady=1, sticky='nesw')
        self.center_frame.grid_rowconfigure(0, weight=2)
        self.center_frame.grid_columnconfigure(1, weight=1)

        self.center_frame.change_western_light(self.texioty_frame)
        self.center_frame.change_eastern_light(self.kinvow_frame)
        self.center_frame.change_southern_light(self.artay_frame)
        self.center_frame.change_northern_light(self.idutc_frame)

        # self.API_helper.txo = self.texioty_frame.texoty


class SpotLighter(tk.LabelFrame):
    """
    A widget for turning visibility on and off for the other widgets.
    """
    def __init__(self, widget_dict: dict, width, height, master=None):
        super().__init__(master, width=width, height=height)
        self.active_light_dict = {}
        self.northern_default = tk.LabelFrame(width=width, height=height*1.325, background=s.rgb_to_hex(s.SAGE_GREEN))
        self.northern_light = self.northern_default
        self.northern_light.grid(column=1, row=0, columnspan=1, rowspan=1, padx=1, pady=3, sticky='n')

        self.eastern_default = tk.LabelFrame(width=width, height=height*3.72, background=s.rgb_to_hex(s.DODGER_BLUE))
        self.eastern_light = self.eastern_default
        self.eastern_light.grid(column=2, row=0, columnspan=1, rowspan=3, padx=1, pady=3, sticky='e')

        self.southern_default = tk.LabelFrame(width=width, height=height*1.325, background=s.rgb_to_hex(s.CRIMSON))
        self.southern_light = self.southern_default
        self.southern_light.grid(column=1, row=2, columnspan=1, rowspan=1, padx=1, pady=3, sticky='s')

        self.western_default = tk.LabelFrame(width=width, height=height*3.72, background=s.rgb_to_hex(s.SANDY_BROWN))
        self.western_light = self.western_default
        self.western_light.grid(column=0, row=0, columnspan=1, rowspan=3, padx=1, pady=3, sticky='w')
        self.widget_dict = widget_dict
        self.init_spotlight_dropdowns()

    def init_spotlight_dropdowns(self):
        """
        Set up and create the dropdowns to determine which widgets go where.
        :return:
        """
        north_light_var = tk.StringVar()
        north_light_var.set('North')
        south_light_var = tk.StringVar()
        south_light_var.set('South')
        east_light_var = tk.StringVar()
        east_light_var.set('East')
        west_light_var = tk.StringVar()
        west_light_var.set('West')
        north_dropdown = tk.OptionMenu(self, north_light_var, *small_widgets,
                                       command=lambda n: self.change_northern_light(self.widget_dict[north_light_var.get()]))
        south_dropdown = tk.OptionMenu(self, south_light_var, *small_widgets,
                                       command=lambda o: self.change_southern_light(self.widget_dict[south_light_var.get()]))
        east_dropdown = tk.OptionMenu(self, east_light_var, *large_widgets,
                                      command=lambda e: self.change_eastern_light(self.widget_dict[east_light_var.get()]))
        west_dropdown = tk.OptionMenu(self, west_light_var, *large_widgets,
                                      command=lambda w: self.change_western_light(self.widget_dict[west_light_var.get()]))
        north_dropdown.grid(column=1, row=0, sticky='n')
        south_dropdown.grid(column=1, row=2, sticky='s')
        east_dropdown.grid(column=2, row=0, rowspan=3, sticky='e')
        west_dropdown.grid(column=0, row=0, rowspan=3, sticky='w')

    def change_northern_light(self, new_widget: tk.Widget):
        """
        Change the northern light to a different small widget.
        :param new_widget: Any small widget.
        :return:
        """
        if new_widget == self.southern_light:
            new_widget = self.northern_default
        self.northern_light.grid(row=3)
        self.northern_light = new_widget
        self.northern_light.grid(column=1, row=0, columnspan=1, rowspan=1, padx=1, pady=3, sticky='n')

    def change_eastern_light(self, new_widget: tk.Widget):
        """
        Change the eastern light to a different large widget.
        :param new_widget: Any large widget.
        :return:
        """
        if new_widget == self.western_light:
            new_widget = self.eastern_default
        self.eastern_light.grid(column=3)
        self.eastern_light = new_widget
        self.eastern_light.grid(column=2, row=0, columnspan=1, rowspan=3, padx=1, pady=3, sticky='e')

    def change_southern_light(self, new_widget: tk.Widget):
        """
        Change the southern light to a different small widget.
        :param new_widget: Any small widget.
        :return:
        """
        if new_widget == self.northern_light:
            new_widget = self.southern_default
        self.southern_light.grid(row=3)
        self.southern_light = new_widget
        self.southern_light.grid(column=1, row=2, columnspan=1, rowspan=1, padx=1, pady=3, sticky='s')

    def change_western_light(self, new_widget: tk.Widget):
        """
        Change the western light to a different large widget.
        :param new_widget: Any large widget.
        :return:
        """
        if new_widget == self.eastern_light:
            new_widget = self.western_default
        self.western_light.grid(column=3)
        self.western_light = new_widget
        self.western_light.grid(column=0, row=0, columnspan=1, rowspan=3, padx=1, pady=3, sticky='w')


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Regular Generator')

    # ~~ ALLOW FOR FULLSCREEN HERE
    # root.attributes("-fullscreen", True)

    # ~~ ALLOW FOR MAX WINDOW HERE
    root.wm_state('zoomed')

    root.configure(background='#0f6faa')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app = Application(screen_width, screen_height, master=root)
    app.mainloop()
