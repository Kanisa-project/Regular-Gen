import math
import random
import tkinter as tk
import settings as s
import artributeCanvas

import idutc


class artributalCanvas(tk.Canvas):
    def __init__(self, width=180, height=180, master=None):
        super(artributalCanvas, self).__init__(master=master, width=width, height=height,
                                               bg=s.rgb_to_hex(s.GHOST_WHITE))
        self.idutc_frame: idutc.IDUTC = master
        self.bind("<Button-1>", self.set_artribute)
        self.bind("<MouseWheel>", self.scroll_through_artribute)
        self.grid_propagate(False)
        self.place(x=340, y=0)
        self.outer_artri_points = s.polypointlist(6, 30, 120, 110, 90)
        self.inner_artri_points = s.polypointlist(6, 30, 120, 110, 30)
        self.menu_polypoints = s.polypointlist(6, 30, 120, 110, 75)
        self.create_polygon(self.outer_artri_points, fill="",
                            outline=s.rgb_to_hex(s.COBALT), width=2)
        self.center_point = (120, 110)
        self.artribute_titles = ["Transparency", "Animation Speed", "Coloration",
                                 "Size", "Motion Range", "Accuracy"]
        self.artyle_artributes_dict = {
            "Data_Source": ["Random", "Human", "Reddit", "OSRS", "Twitter", "Discord"],
            "Transparency": ["Door", "Window"],
            "Animation Speed": ["Ice", "Fire"],
            "Coloration": ["Rainbow", "Cloud"],
            "Size": ["Chicken", "Dog", "Camel"],
            "Motion Range": ["Sock", "Rock"],
            "Accuracy": ["Pen", "Crayon"]
        }

        self.artributeMenus = self.artyle_artributes_dict
        self.update_center_point()
        self.initiate_artribute_menus()
        self.selected_artribute = "Size"
        self.selected_index = 3

    def initiate_artribute_menus(self):
        print(self.artyle_artributes_dict)
        for key, value in self.artyle_artributes_dict.items():
            attribute_str_var = tk.StringVar()
            attribute_str_var.set(random.choice(value))
            if key == "Data_Source":
                # ~~ set data_source to what you want
                attribute_str_var.set("Random")
            elif key == "Size":
                # ~~ set size to what you want
                attribute_str_var.set("Dog")
            self.artributeMenus[key] = [attribute_str_var,
                                        tk.OptionMenu(self, attribute_str_var, *value)]
            polypoint_index = list(self.artyle_artributes_dict.keys()).index(key)
            # print("WINFO", self.artributeMenus[key][1].winfo_width())
            self.artributeMenus[key][1].place(x=self.outer_artri_points[polypoint_index][0],
                                              y=self.outer_artri_points[polypoint_index][1])
            self.update()
            self.artributeMenus[key][1].place_configure(
                x=self.menu_polypoints[polypoint_index][0] - (self.artributeMenus[key][1].winfo_width() // 2),
                y=self.menu_polypoints[polypoint_index][1] - 18 + 200)
        print(self.artributeMenus, "DONE")

    def set_artribute(self, event):
        self.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="black", width=3)
        click_point = (event.x, event.y)
        distance = math.sqrt((120-click_point[0]) ** 2 + (110 - click_point[1]) ** 2)
        self.inner_artri_points = s.polypointlist(6, 30, 120, 110, int(distance+10))
        self.update_center_point()

    def update_center_point(self):
        self.delete('all')
        self.create_polygon(self.outer_artri_points, fill="",
                            outline=s.rgb_to_hex(s.COBALT), width=2)
        self.create_polygon(self.inner_artri_points, fill=s.rgb_to_hex(s.COBALT),
                            outline=s.rgb_to_hex(s.COBALT), width=2)
        for i, point in enumerate(self.outer_artri_points):
            artribute_title = list(self.artyle_artributes_dict.keys())[i]
            artributal_emoji = artribute_emoji(self.artyle_artributes_dict[artribute_title][0])
            self.create_text(point, text=artributal_emoji, fill='black', font=("Times New Roman", 20))
            self.create_line(self.inner_artri_points[i], point, fill=s.rgb_to_hex(s.CRIMSON), width=2)
            # self.idutc_frame.kre8dict['artributes'] = self.artyle_artributes_dict[artribute_title][0]

    def scroll_through_artribute(self, event):
        self.delete("select_circle")
        self.selected_index = s.clamp(self.selected_index - event.delta // 120, 0, 5, True)
        self.selected_artribute = self.artribute_titles[self.selected_index]
        # print(self.selected_artribute, event.delta//120)
        self.create_oval(self.outer_artri_points[self.selected_index][0] - 16,
                         self.outer_artri_points[self.selected_index][1] - 16,
                         self.outer_artri_points[self.selected_index][0] + 16,
                         self.outer_artri_points[self.selected_index][1] + 16,
                         outline=s.rgb_to_hex(s.DARK_GREEN), width=2, tags="select_circle")


def artribute_emoji(keeword: str) -> str:
    emoji_text = ""
    if not isinstance(keeword, str):
        keeword = keeword.get()
    print(keeword, "KEEWORD")
    if "Door" in keeword:
        emoji_text = "🚪"
    elif "Window" in keeword:
        emoji_text = "🪟"
    elif "Cloud" in keeword:
        emoji_text = "☁️"
    elif "Rainbow" in keeword:
        emoji_text = "🌈"
    elif "Fire" in keeword:
        emoji_text = "🔥"
    elif "Ice" in keeword:
        emoji_text = "🧊"
    elif "Camel" in keeword:
        emoji_text = "🐫"
    elif "Chicken" in keeword:
        emoji_text = "🐓"
    elif "Dog" in keeword:
        emoji_text = "🐶"
    elif "Rock" in keeword:
        emoji_text = "🗿"
    elif "Sock" in keeword:
        emoji_text = "🧦"
    elif "Crayon" in keeword:
        emoji_text = "🖍️"
    elif "Pen" in keeword:
        emoji_text = "🖋"
    return emoji_text


def plan_angled_line(x, y, angle, length, width, color):
    """
    Plan a line's properties.

    @param color: color of the line
    @param x: start x position
    @param y: start y position
    @param angle: angle to draw line
    @param length: length of line to draw
    @param width: thickness of line
    @return:
    """
    endx1 = x
    endy1 = y
    endx2 = x + length * math.cos(math.radians(angle + 180)) * -1
    endy2 = y + length * math.sin(math.radians(angle + 180)) * -1
    return (s.clamp(endx1, 0, 240),
            s.clamp(endy1, 0, 400),
            s.clamp(endx2, 0, 240),
            s.clamp(endy2, 0, 400)), width, color
