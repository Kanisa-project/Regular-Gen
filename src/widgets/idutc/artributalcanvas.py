import math
import tkinter as tk
from src.settings import themery as t
from src.utils import helpers

from src.widgets import idutc

ARTRIMOJI = {
    "Door": '🚪',
    "Window": '🪟',
    "Cloud": '☁',
    "Rainbow": '🌈',
    "Fire": '🔥',
    "Ice": '🧊',
    "Camel": '🐫',
    "Chicken": '🐓',
    "Rock": '🗿',
    "Sock": '🧦',
    "Crayon": '🖍',
    "Pen": '🖋',
    "Confetti": '🎊',
    "Mosaic": '🧱',
    "Butterfly": '🦋',
    "Sponge": '🧽',
    "Metal": '🛡️',
    "Petal": '🌷',
    "Printer": '🖨️',
    "Stamp": '📠'
}

class ArtributalCanvas(tk.Canvas):
    def __init__(self, width=180, height=180, master=None):
        """
        Canvas
        :param width:
        :param height:
        :param master:
        """
        super(ArtributalCanvas, self).__init__(master=master, width=width, height=height,
                                               bg=t.rgb_to_hex(t.GHOST_WHITE))
        self.idutc_frame: idutc.IDUTC = master
        self.center_point = (width//2, width//2)
        self.bind("<Button-1>", self.set_artribute)
        self.bind("<MouseWheel>", self.scroll_through_artribute)
        self.grid_propagate(False)
        self.artribute_titles = ["one-more_extra_filler_bad_code", "Transparency", "Coloration", "Animation Speed", "Size", "Motion Range",
                                   "Accuracy", "Structure", "Symmetry", "Material Rigidity", "Repetition"]
        self.outer_artri_points = helpers.polypointlist(len(self.artribute_titles)-1, 18, int(self.center_point[0]), int(self.center_point[1]), int(width * .45))
        self.inner_radius = 30
        self.inner_artri_points = self._build_inner_points()
        self.create_polygon(self.outer_artri_points,
                            outline=t.rgb_to_hex(t.COBALT), width=2)
        self.artyle_artributes_dict = {
            "Data_Source": ["Random", "Human", "Reddit", "OSRS", "Twitter", "Discord"],
            "Transparency": ["Door", "Window"],
            "Coloration": ["Rainbow", "Cloud"],
            "Animation Speed": ["Ice", "Fire"],
            "Size": ["Chicken", "Camel"],
            "Motion Range": ["Sock", "Rock"],
            "Accuracy": ["Pen", "Crayon"],
            "Structure": ["Confetti", "Mosaic"],
            "Symmetry": ["Butterfly", "Sponge"],
            "Material Rigidity": ["Metal", "Petal"],
            "Repetition": ["Printer", "Stamp"]
        }
        self.update_center_point()
        self.selected_artribute = "Size"
        self.selected_index = 3

    def set_artribute(self, event):
        # self.create_oval(event.x - 3, event.y - 3, event.x + 3, event.y + 3, fill="black", width=3)
        click_point = (event.x, event.y)
        distance = helpers.clamp(math.sqrt((self.center_point[0]-click_point[0]) ** 2 + (self.center_point[1] - click_point[1]) ** 2), 0, 80)
        self.inner_radius = int(distance + 10)
        self.inner_artri_points = self._build_inner_points()
        self.update_center_point()

    def gather_artribute_length(self, artri_title: str) -> int:
        if artri_title in list(self.idutc_frame.slider_dict.keys()):
            return int(self.idutc_frame.slider_dict[artri_title][0].get())
        else:
            return 0

    def update_center_point(self):
        self.delete('all')
        self.create_polygon(self.outer_artri_points, fill="",
                            outline=t.rgb_to_hex(t.COBALT), width=2)

        n = len(self.inner_artri_points)
        if n >= 3:
            for i in range(n):
                p1 = self.inner_artri_points[i]
                p2 = self.inner_artri_points[(i + 1) % n]
                edge_color = self._edge_color_for_index(i)
                print(self.idutc_frame.kre8dict['artributes'])
                if "Cloud" in self.idutc_frame.kre8dict['artributes']:
                    print("Clouding...")
                    shade_lvl = 255 // len(self.idutc_frame.kre8dict['artributes'])
                    edge_color = t.rgb_to_hex((shade_lvl * i, shade_lvl * i, shade_lvl * i))
                self.create_polygon(p1, p2, self.center_point, fill=edge_color)

        self.create_polygon(self.inner_artri_points, fill='',
                            outline='', width=2)
        for i, point in enumerate(self.outer_artri_points):
            print(i, "->", point, self.artribute_titles[i])
            artribute_title = self.artribute_titles[i]
            artributal_emoji = ARTRIMOJI[list(self.idutc_frame.kre8dict['artributes'].keys())[i-1]]
            # artributal_emoji = artribute_emoji(self.idutc_frame.kre8dict['artributes'][i])
            self.create_text(point, text=artributal_emoji, fill='black', font=("Times New Roman", 16))
            dx = self.center_point[0] - point[0]
            dy = self.center_point[1] - point[1]
            angle_to_center = math.degrees(math.atan2(dy, dx))
            if angle_to_center < 0:
                angle_to_center += 360
            artri_line_tup = plan_angled_line(point[0], point[1], angle_to_center,
                                              self.gather_artribute_length(artribute_title), 3, 'black')
            self.create_line(artri_line_tup[0][0], artri_line_tup[0][1],
                             artri_line_tup[0][2], artri_line_tup[0][3], fill=t.rgb_to_hex(t.CRIMSON), width=2)

    def sync_with_use_id(self):
        self.inner_artri_points = self._build_inner_points()
        self.update_center_point()

    def scroll_through_artribute(self, event):
        self.delete("select_circle")
        self.selected_index = helpers.clamp(self.selected_index - event.delta // 120, 0, 5, True)
        self.selected_artribute = self.artribute_titles[self.selected_index]
        self.create_oval(self.outer_artri_points[self.selected_index][0] - 16,
                         self.outer_artri_points[self.selected_index][1] - 16,
                         self.outer_artri_points[self.selected_index][0] + 16,
                         self.outer_artri_points[self.selected_index][1] + 16,
                         outline=t.rgb_to_hex(t.DARK_GREEN), width=2, tags="select_circle")

    def _get_use_id(self) -> str:
        try:
            return self.idutc_frame.id_entry.get()
        finally:
            return self.idutc_frame.kre8dict.get("use_id", "")

    def _build_inner_points(self):
        use_id = self._get_use_id()
        id_len = max(3, len(use_id))
        return helpers.polypointlist(id_len, 90, int(self.center_point[0]), int(self.center_point[1]), int(self.inner_radius))

    def _letter_rgb(self, ch: str) -> tuple:
        c = ch.lower()
        if c in t.ALPHANUMERIC_COLORS:
            return t.ALPHANUMERIC_COLORS[c]
        return getattr(theme, "PUNCTUATION_COLORS", {}).get(c, (0, 0, 0))

    def _edge_color_for_index(self, idx: int) -> str:
        use_id = self._get_use_id()
        if not use_id:
            return t.rgb_to_hex(t.DARK_GREEN)
        ch = use_id[idx % len(use_id)]
        rgb = self._letter_rgb(ch)
        return t.rgb_to_hex(rgb)

def artribute_emoji(keeword) -> str:
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
    # elif "Dog" in keeword:
    #     emoji_text = "🐶"
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
    return (helpers.clamp(endx1, 0, 240),
            helpers.clamp(endy1, 0, 400),
            helpers.clamp(endx2, 0, 240),
            helpers.clamp(endy2, 0, 400)), width, color
