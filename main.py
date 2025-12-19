import sys
import tkinter as tk
from src.widgets import kinvow, idutc, artay, kalendar, glythph, wordie, spirite_forge
from src.widgets.cooked_book.cooked_book import CookedBook
from src.widgets.foto_worx.tab_foto import FotoWorx
from src.widgets.mujica.mujica import Mujica
from src.widgets.py_launcher.launchrr import Launchrr
from src.widgets.texioty import texioty
from src.settings import themery as t

large_widgets = ["Texioty", "Kinvow", "Cooked Book", "Mujica",
                 "Foto Worx"]
small_widgets = ["Calendar", "Wordie", "IDUTC",
                 "Launchrr", "Glythph", "Spirite Forge"]

def run_pygame_game(gaim_for_launch):
    """Run a simple pygame demo loop until the user quits pygame.
       This function runs on the main thread and blocks until pygame quits.
    """
    print(f"Launching game: {gaim_for_launch}")
    gaim_for_launch("Bluebeard").run()

class Application(tk.Frame):
    def __init__(self, screen_w: int, screen_h: int, master=None):
        """
        Primary application window with all the widgets required.
        :param master:
        """
        super().__init__(master)
        sml_width = screen_w * .333
        sml_height = screen_h * .4
        lrg_width = screen_w * .32
        lrg_height = screen_h * .96
        self.texioty_frame = texioty.Texioty(width=lrg_width, height=lrg_height)

        self.idutc_frame = idutc.IDUTC(width=sml_width, height=sml_height, master=self.texioty_frame)

        self.artay_frame = artay.ARTAY(width=sml_width, height=sml_height, idutc_frame=self.idutc_frame)

        self.kinvow_frame = kinvow.KINVOW(width=lrg_width, height=lrg_height,
                                          idutc_frame=self.idutc_frame, artay_frame=self.artay_frame)
        self.kinvow_frame.txo = self.texioty_frame.texoty

        self.glythph_frame = glythph.Glythph(width=sml_width, height=sml_height, master=self.texioty_frame)
        self.wordie_frame = wordie.Wordie(width=sml_width, height=sml_height,
                                          master=self.texioty_frame, kinvow_size=(self.kinvow_frame.canvas_w//8, self.kinvow_frame.canvas_h//4))
        self.spirite_forge_frame = spirite_forge.SpiriteForge(width=sml_width, height=sml_height, master=self.texioty_frame)

        self.calendar_frame = kalendar.Kalendar(width=sml_width, height=sml_height)
        self.calendar_frame.txo = self.texioty_frame.texoty

        self.launchrr_frame = Launchrr(width=sml_width, height=sml_height, master=self.texioty_frame, tk_root_window=master)
        self.cookbook_frame = CookedBook(width=lrg_width, height=lrg_height, master=self.texioty_frame)
        self.mujica_frame = Mujica(width=lrg_width, height=lrg_height, master=self.texioty_frame)
        self.foto_worx_frame = FotoWorx(width=lrg_width, height=lrg_height, master=self.texioty_frame)

        print("Created the main frame helper widgets..")

        self.texioty_frame.add_helper_widget("CLDR", self.calendar_frame)
        self.texioty_frame.add_helper_widget("IDUT", self.idutc_frame)
        self.texioty_frame.add_helper_widget("KNVO", self.kinvow_frame)
        self.texioty_frame.add_helper_widget("ARTY", self.artay_frame)
        self.texioty_frame.add_helper_widget("THPH", self.glythph_frame)
        self.texioty_frame.add_helper_widget("WRDR", self.wordie_frame)
        self.texioty_frame.add_helper_widget("GAIM", self.launchrr_frame)
        self.texioty_frame.add_helper_widget("SPII", self.spirite_forge_frame)
        self.texioty_frame.add_helper_widget("COOK", self.cookbook_frame)
        self.texioty_frame.add_helper_widget("MUJI", self.mujica_frame)
        self.texioty_frame.add_helper_widget("FOTO", self.foto_worx_frame)
        print("Added the main frame helpers..")

        self.widget_dict = {
            "Texioty": self.texioty_frame,
            "Calendar": self.calendar_frame,
            "IDUTC": self.idutc_frame,
            "Kinvow": self.kinvow_frame,
            "aRtay": self.artay_frame,
            "Wordie": self.wordie_frame,
            "Glythph": self.glythph_frame,
            "Spirite Forge": self.spirite_forge_frame,
            "Launchrr": self.launchrr_frame,
            "Cooked Book": self.cookbook_frame,
            "Mujica": self.mujica_frame,
            "Foto Worx": self.foto_worx_frame
        }
        self.center_frame = SpotLighter(widget_dict=self.widget_dict, width=screen_w//3, height=screen_h//4)
        self.center_frame.grid(column=1, row=1, columnspan=1, rowspan=1, padx=1, pady=1, sticky='nesw')
        self.center_frame.grid_rowconfigure(0, weight=2)
        self.center_frame.grid_columnconfigure(1, weight=1)

        self.center_frame.change_western_light(self.texioty_frame)
        self.center_frame.change_eastern_light(self.mujica_frame)
        self.center_frame.change_southern_light(self.spirite_forge_frame)
        self.center_frame.change_northern_light(self.launchrr_frame)

        self.texioty_frame.log_profile_in('bluebeard', "p455")



class SpotLighter(tk.LabelFrame):
    """
    A widget for turning visibility on and off for the other widgets.
    """
    def __init__(self, widget_dict: dict, width, height, master=None):
        super().__init__(master, width=width, height=height)
        self.active_light_dict = {}
        self.northern_default = tk.LabelFrame(width=width, height=height, background=t.rgb_to_hex(t.SAGE_GREEN))
        self.northern_light = self.northern_default
        self.northern_light.grid(column=1, row=0, columnspan=1, rowspan=1, padx=1, pady=3, sticky='n')

        self.eastern_default = tk.LabelFrame(width=width, height=height, background=t.rgb_to_hex(t.DODGER_BLUE))
        self.eastern_light = self.eastern_default
        self.eastern_light.grid(column=2, row=0, columnspan=1, rowspan=3, padx=1, pady=3, sticky='e')

        self.southern_default = tk.LabelFrame(width=width, height=height, background=t.rgb_to_hex(t.CRIMSON))
        self.southern_light = self.southern_default
        self.southern_light.grid(column=1, row=2, columnspan=1, rowspan=1, padx=1, pady=3, sticky='s')

        self.western_default = tk.LabelFrame(width=width, height=height, background=t.rgb_to_hex(t.SANDY_BROWN))
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
        north_light_var.set('Launchrr')
        south_light_var = tk.StringVar()
        south_light_var.set('Spirite Forge')
        east_light_var = tk.StringVar()
        east_light_var.set('Kinvow')
        west_light_var = tk.StringVar()
        west_light_var.set('Texioty')
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
        self.northern_light.grid(column=1, row=0, columnspan=1, rowspan=1, padx=1, pady=3, sticky='s')

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
        self.eastern_light.grid(column=2, row=0, columnspan=1, rowspan=3, padx=6, pady=3, sticky='e')

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
        self.southern_light.grid(column=1, row=2, columnspan=1, rowspan=1, padx=1, pady=3, sticky='n')

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
        self.western_light.grid(column=0, row=0, columnspan=1, rowspan=3, padx=6, pady=3, sticky='w')


def build_app() -> Application:
    # global root
    root = tk.Tk()
    root.title('kanisaGen - v0.11.02')
    print("Title loaded...")

    # ~~ ALLOW FOR FULLSCREEN HERE
    root.wm_attributes("-fullscreen", 'True')

    # ~~ ALLOW FOR MAX WINDOW HERE
    # root.wm_state('zoomed')

    root.configure(background='#0f6faa')
    print("Background configured...")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    print("Setting screen dimensions to ", screen_width, screen_height, "....")
    app = Application(screen_width, screen_height, master=root)
    print("app becoming Application....")
    return app

def main():
    main_app = build_app()
    while main_app:
        try:
            main_app.mainloop()
        except Exception as e:
            print("Problem with main_app", e)
            break

        _launch_game_requested = main_app.launchrr_frame.launch_gaim_flag
        main_app.launchrr_frame.launch_gaim_flag = False

        if _launch_game_requested and main_app.launchrr_frame.loaded_gaim:
            _launch_game_requested = False
            run_pygame_game(main_app.launchrr_frame.loaded_gaim)
        else:
            break
        print("MAINAPP", main_app)

    sys.exit(0)



if __name__ == '__main__':
    main()
    # run_pygame_game()