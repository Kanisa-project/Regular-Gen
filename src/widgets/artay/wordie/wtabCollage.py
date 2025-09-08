import math
import random

from . import wordieTab
from src.settings import theme
from src.utils import helpers
from typing import Tuple

from typing import Dict

import os
import tkinter as tk
from typing import Optional, Callable, List


class FontCanvas(tk.Canvas):
    """
    A simple canvas that loads 10 fonts from assets/Fonts and displays them as clickable text previews.
    """

    def __init__(self, master=None, width=133, height=200, bg="#ffffff"):
        super().__init__(master=master, width=width, height=height, bg=bg, highlightthickness=0)

        self.font_directory = os.getcwd() + "/filesInput/fonts/"
        self.sample_text = "Sample Text Abc123"
        self.font_size = 10
        self.selected_font: Optional[str] = None
        self.selection_callback: Optional[Callable[[str, str], None]] = None

        # Storage for fonts and their canvas text items
        self.font_paths: List[str] = []
        self.font_names: List[str] = []
        self.text_items: List[int] = []

        # Load and display fonts
        self._load_fonts()
        self._create_font_previews()

        # Bind click events
        self.bind("<Button-1>", self._on_click)

    def _load_fonts(self):
        """Load up to 5 TTF fonts from the assets/Fonts directory."""
        if not os.path.exists(self.font_directory):
            return

        ttf_files = [f for f in os.listdir(self.font_directory) if f.lower().endswith('.ttf')]
        random.shuffle(ttf_files)

        for i, filename in enumerate(ttf_files[:9]):
            font_path = os.path.join(self.font_directory, filename)
            font_name = os.path.splitext(filename)[0]
            self.font_paths.append(font_path)
            self.font_names.append(font_name)

    def _create_font_previews(self):
        """Create clickable text previews for each font on the canvas."""
        y_spacing = 22
        start_y = 16

        for i, font_name in enumerate(self.font_names):
            y_pos = start_y + (i * y_spacing)

            # Create text item with fallback to system fonts
            # Since tkinter can't directly load TTF files, we'll use font names
            try:
                # Try to use a reasonable fallback font
                display_font = (font_name, self.font_size)
                text = f"{font_name}"
                font_color = "#333333"
            except:
                display_font = ("TkDefaultFont", self.font_size)
                text = f"{font_name}"
                font_color = "#AE6942"

            text_id = self.create_text(
                16, y_pos,
                text=text,
                font=display_font,
                fill=font_color,
                anchor="w",
                tags=(f"font:{font_name}", "clickable")
            )

            self.text_items.append(text_id)

            # Add a subtle background rectangle for better clicking
            bbox = self.bbox(text_id)
            if bbox:
                rect_id = self.create_rectangle(
                    bbox[0] - 5, bbox[1] - 2, bbox[2] + 5, bbox[3] + 2,
                    fill="", outline="", width=0,
                    tags=(f"bg:{font_name}", "clickable")
                )
                # Lower the rectangle behind the text
                self.tag_lower(rect_id)

    def _on_click(self, event):
        """Handle click events on font previews."""
        # Find the clicked item
        clicked_item = self.find_closest(event.x, event.y)[0]
        tags = self.gettags(clicked_item)
        print(clicked_item)
        # Extract font name from tags
        font_name = None
        for tag in tags:
            if tag.startswith("font:"):
                font_name = tag[5:]  # Remove "font:" prefix
                break
            elif tag.startswith("bg:"):
                font_name = tag[3:]  # Remove "bg:" prefix
                break

        if font_name and font_name in self.font_names:
            self._select_font(font_name)

    def _select_font(self, font_name: str):
        """Select a font and update visual feedback."""
        # Clear previous selection
        self._clear_selection()

        # Set new selection
        self.selected_font = font_name
        font_index = self.font_names.index(font_name)
        font_path = self.font_paths[font_index]

        # Highlight selected font
        for tag in [f"font:{font_name}", f"bg:{font_name}"]:
            items = self.find_withtag(tag)
            for item in items:
                if self.type(item) == "text":
                    self.itemconfig(item, fill="#0066cc", font=(font_name, self.font_size, "bold"))
                elif self.type(item) == "rectangle":
                    self.itemconfig(item, fill="#e6f3ff", outline="#0066cc", width=1)

        # Call selection callback if set
        if self.selection_callback:
            self.selection_callback(font_name, font_path)

    def _clear_selection(self):
        """Clear current selection visual feedback."""
        if self.selected_font:
            # Reset previous selection appearance
            old_tags = [f"font:{self.selected_font}", f"bg:{self.selected_font}"]
            for tag in old_tags:
                items = self.find_withtag(tag)
                for item in items:
                    if self.type(item) == "text":
                        self.itemconfig(item, fill="#333333", font=(self.selected_font, self.font_size))
                    elif self.type(item) == "rectangle":
                        self.itemconfig(item, fill="", outline="", width=0)

    def set_selection_callback(self, callback: Callable[[str, str], None]):
        """Set callback function that receives (font_name, font_path) when font is selected."""
        self.selection_callback = callback

    def get_selected_font(self) -> Optional[tuple]:
        """Get currently selected font as (font_name, font_path) or None."""
        if self.selected_font and self.selected_font in self.font_names:
            font_index = self.font_names.index(self.selected_font)
            return (self.selected_font, self.font_paths[font_index])
        return None

    def select_font_by_name(self, font_name: str) -> bool:
        """Programmatically select a font by name."""
        if font_name in self.font_names:
            self._select_font(font_name)
            return True
        return False

class GraphCanvas(tk.Canvas):
    """
    A small utility canvas to:
    - create points and lines
    - keep stable references to them
    - support selection and dragging
    - notify an external side panel via a callback

    Conventions:
    - Points have tag 'point'
    - Lines have tag 'line'
    - Selections highlighted with a temporary 'selection' overlay
    - Lines connect two point names (endpoints)
    """

    def __init__(self, master=None, width=200, height=300, bg=theme.rgb_to_hex(theme.RANDOM_COLOR3)):
        super().__init__(master=master, width=width, height=height, bg=bg, highlightthickness=0)
        self._sidepanel_callback: Optional[Callable[[str, dict], None]] = None

        # Storage
        # points[name] = {"id": int, "x": float, "y": float, "r": int, "fill": str}
        self.points: Dict[str, Dict] = {}

        # lines[name] = {"id": int, "p1": str, "p2": str, "width": int, "fill": str}
        self.lines: Dict[str, Dict] = {}

        # Interaction state
        self._selected_item: Optional[int] = None
        self._selection_overlay_id: Optional[int] = None
        self._dragging_point_name: Optional[str] = None
        self._pending_line_start_point: Optional[str] = None  # shift+click to start/finish a line

        # Bindings
        self.bind("<Button-1>", self._on_left_click)
        self.bind("<Button-2>", self._on_middle_click)
        self.bind("<Button-3>", self._on_right_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)

        # For shift detection consistently on platforms
        self.bind_all("<KeyPress-Shift_L>", lambda e: None)
        self.bind_all("<KeyPress-Shift_R>", lambda e: None)

    # ---------------- Public API ----------------

    def set_sidepanel_callback(self, callback: Callable[[str, dict], None]):
        """
        Provide a callback that receives events from the canvas to update your side panel.
        Example signature: callback(event_type: str, payload: dict)

        Event types may include:
        - "point_created": {"name": str, "x": float, "y": float}
        - "line_created": {"name": str, "p1": str, "p2": str}
        - "selected": {"kind": "point"|"line", "name": str}
        - "point_moved": {"name": str, "x": float, "y": float}
        """
        self._sidepanel_callback = callback

    def add_point(self, name: str, x: float, y: float, r: int = 4, fill: str = "#202020"):
        if name in self.points:
            raise ValueError(f"Point '{name}' already exists")
        pid = self.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline="", tags=("point", f"point:{name}"))
        self.points[name] = {"id": pid, "x": x, "y": y, "r": r, "fill": fill}
        self._notify("point_created", {"name": name, "x": x, "y": y})
        return pid

    def add_line(self, name: str, p1_name: str, p2_name: str, width: int = 2, fill: str = "#0066cc"):
        if name in self.lines:
            raise ValueError(f"Line '{name}' already exists")
        if p1_name not in self.points or p2_name not in self.points:
            raise ValueError("Both endpoints must be existing point names")
        p1 = self.points[p1_name]
        p2 = self.points[p2_name]
        lid = self.create_line(p1["x"], p1["y"], p2["x"], p2["y"], width=width, fill=fill,
                               tags=("line", f"line:{name}"))
        self.lines[name] = {"id": lid, "p1": p1_name, "p2": p2_name, "width": width, "fill": fill}
        self.tag_lower(lid)  # ensure lines are behind points
        self._notify("line_created", {"name": name, "p1": p1_name, "p2": p2_name})
        return lid

    def select_by_name(self, kind: str, name: str):
        if kind == "point":
            item_id = self._get_point_id(name)
        elif kind == "line":
            item_id = self._get_line_id(name)
        else:
            raise ValueError("kind must be 'point' or 'line'")
        self._select_item(item_id)
        self._notify("selected", {"kind": kind, "name": name})

    def move_point(self, name: str, x: float, y: float):
        if name not in self.points:
            raise ValueError(f"Point '{name}' not found")
        self.points[name]["x"], self.points[name]["y"] = x, y
        pid = self.points[name]["id"]
        r = self.points[name]["r"]
        self.coords(pid, x - r, y - r, x + r, y + r)
        self._update_lines_for_point(name)
        self._notify("point_moved", {"name": name, "x": x, "y": y})

    def get_point_coords(self, name: str) -> Tuple[float, float]:
        p = self.points[name]
        return p["x"], p["y"]

    def get_selection_info(self) -> Optional[dict]:
        """Return currently selected item info or None."""
        if self._selected_item is None:
            return None
        tags = self.gettags(self._selected_item)
        if "point" in tags:
            name = self._extract_tag_value(tags, "point:")
            return {"kind": "point", "name": name}
        if "line" in tags:
            name = self._extract_tag_value(tags, "line:")
            return {"kind": "line", "name": name}
        return None

    # ---------------- Internal helpers ----------------

    def _get_point_id(self, name: str) -> int:
        return self.points[name]["id"]

    def _get_line_id(self, name: str) -> int:
        return self.lines[name]["id"]

    @staticmethod
    def _extract_tag_value(tags, prefix: str) -> Optional[str]:
        for t in tags:
            if t.startswith(prefix):
                return t[len(prefix):]
        return None

    def _notify(self, event_type: str, payload: dict):
        if self._sidepanel_callback:
            try:
                self._sidepanel_callback(event_type, payload)
            except Exception:
                # Keep canvas responsive even if side panel errors
                pass

    def _update_lines_for_point(self, point_name: str):
        for lname, lin in self.lines.items():
            if lin["p1"] == point_name or lin["p2"] == point_name:
                p1 = self.points[lin["p1"]]
                p2 = self.points[lin["p2"]]
                self.coords(lin["id"], p1["x"], p1["y"], p2["x"], p2["y"])

    def _clear_selection_overlay(self):
        if self._selection_overlay_id and self.find_withtag(self._selection_overlay_id):
            self.delete(self._selection_overlay_id)
        self._selection_overlay_id = None

    def _select_item(self, item_id: Optional[int]):
        if item_id == self._selected_item:
            return
        self._clear_selection_overlay()
        self._selected_item = item_id
        if item_id is None:
            return
        tags = self.gettags(item_id)
        if "point" in tags:
            # Draw a ring around the point
            name = self._extract_tag_value(tags, "point:")
            x, y = self.points[name]["x"], self.points[name]["y"]
            r = self.points[name]["r"] + 4
            self._selection_overlay_id = self.create_oval(
                x - r, y - r, x + r, y + r,
                outline="#22aa22", width=2, dash=(3, 2)
            )
        elif "line" in tags:
            # Draw a slightly thicker overlay line
            x1, y1, x2, y2 = self.coords(item_id)
            self._selection_overlay_id = self.create_line(
                x1, y1, x2, y2, width=4, fill="#22aa22"
            )
            self.tag_lower(self._selection_overlay_id)

    # ---------------- Event handlers ----------------

    def _hit_test_point_name(self, x: float, y: float) -> Optional[str]:
        # Small area to find a nearby point
        padding = 6
        items = self.find_overlapping(x - padding, y - padding, x + padding, y + padding)
        for it in items:
            tags = self.gettags(it)
            if "point" in tags:
                return self._extract_tag_value(tags, "point:")
        return None

    def _hit_test_line_name(self, x: float, y: float) -> Optional[str]:
        # Lines are thin; use a small rectangle around click to find one
        padding = 4
        items = self.find_overlapping(x - padding, y - padding, x + padding, y + padding)
        for it in items:
            tags = self.gettags(it)
            if "line" in tags:
                return self._extract_tag_value(tags, "line:")
        return None

    def _on_left_click(self, event: tk.Event):
        x, y = float(event.x), float(event.y)
        shift = (event.state & 0x0001) != 0  # Shift mask

        point_name = self._hit_test_point_name(x, y)
        line_name = self._hit_test_line_name(x, y)

        if shift:
            # Shift-click: create or finish a line between points
            if point_name:
                if self._pending_line_start_point is None:
                    self._pending_line_start_point = point_name
                    self._select_item(self.points[point_name]["id"])
                else:
                    start = self._pending_line_start_point
                    end = point_name
                    if start != end:
                        # Create a unique line name
                        base = f"{start}->{end}"
                        name = base
                        idx = 1
                        while name in self.lines:
                            idx += 1
                            name = f"{base}#{idx}"
                        self.add_line(name, start, end)
                        self._select_item(self.lines[name]["id"])
                    self._pending_line_start_point = None
            else:
                # Shift-click empty space cancels pending start
                self._pending_line_start_point = None
                self._select_item(None)
            return

        # Normal click
        if point_name:
            self._dragging_point_name = point_name
            self._select_item(self.points[point_name]["id"])
            self._notify("selected", {"kind": "point", "name": point_name})
            return

        if line_name:
            self._select_item(self.lines[line_name]["id"])
            self._notify("selected", {"kind": "line", "name": line_name})
            return

        # Empty area: create a new point with an auto name
        auto_name = self._next_point_name()
        self.add_point(auto_name, x, y)
        self._select_item(self.points[auto_name]["id"])
        self._dragging_point_name = auto_name  # allow immediate drag after placing

    def _on_drag(self, event: tk.Event):
        if self._dragging_point_name is None:
            return
        x, y = float(event.x), float(event.y)
        self.move_point(self._dragging_point_name, x, y)

        # Refresh selection ring if present
        if self._selection_overlay_id:
            self._select_item(self.points[self._dragging_point_name]["id"])

    def _on_release(self, event: tk.Event):
        self._dragging_point_name = None

    # ---------------- Utilities ----------------

    def _next_point_name(self) -> str:
        base = "P"
        idx = 1
        while f"{base}{idx}" in self.points:
            idx += 1
        return f"{base}{idx}"

    def _on_right_click(self, event: tk.Event):
        self.points: Dict[str, Dict] = {}
        self.lines: Dict[str, Dict] = {}
        self.delete('all')
        self.master.update_graph_drawn_lines()

    def _on_middle_click(self, event: tk.Event):
        self.points: Dict[str, Dict] = {}
        self.lines: Dict[str, Dict] = {}
        self.delete('all')
        self.master.randomize_graph_drawn_lines()


class Collage(wordieTab.Wordietab):
    def __init__(self, master=None, masterpiece_size=(1000, 500)):
        super().__init__(master=master)
        self.textbox_names = ["One", "Two", "Three"]
        self.collage_name_dict = init_collage_areas(self.textbox_names)
        self.setup_button_choices(["R a n D O c A p S p A c E D"], start_y_cell=0, start_x_cell=1)
        self.setup_text_boxes(self.collage_name_dict, start_y_cell=2, width=28)
        self.button_dict["R a n D O c A p S p A c E D"][1].config(command=self.shuffle_case_the_areas)
        for area in self.textbox_names:
            self.textbox_dict[area][0].set(helpers.random_loading_phrase())
        self.graph_canvas = GraphCanvas(self, width=masterpiece_size[0]//3, height=masterpiece_size[1]//3)
        self.graph_canvas.grid(row=0, column=0, rowspan=25, sticky="nsew")
        self.font_canvas = FontCanvas(self)
        self.font_canvas.grid(row=5, column=1, rowspan=1, sticky="nsew")
        self.update_graph_drawn_lines()

    def get_font_canvas_selection(self):
        pass

    def get_graph_canvas_points(self) -> dict:
        points = {}
        for area in self.textbox_names:
            this_point = self.graph_canvas.get_point_coords(area+"-P0")
            that_point = self.graph_canvas.get_point_coords(area+"-P1")
            points[area] = [(int(this_point[0]*5), int(this_point[1]*5)), int(helpers.angle_between_points(this_point, that_point)),
                            (int(that_point[0]), int(that_point[1])), int(math.dist(this_point, that_point)), self.font_canvas.selected_font]
        return points

    def update_graph_drawn_lines(self):
        for textbox in self.textbox_names:
            self.graph_canvas.add_point(textbox+"-P0", 20, 20*(self.textbox_names.index(textbox)+3))
            self.graph_canvas.add_point(textbox+"-P1", 80, 20*(self.textbox_names.index(textbox)+3))
            self.graph_canvas.add_line(textbox+"-L0", textbox+"-P0", textbox+"-P1")

    def randomize_graph_drawn_lines(self):
        for textbox in self.textbox_names:
            self.graph_canvas.add_point(textbox+"-P0", random.randint(0, self.graph_canvas.winfo_width()),
                                        random.randint(0, self.graph_canvas.winfo_height()))
            self.graph_canvas.add_point(textbox+"-P1", random.randint(0, self.graph_canvas.winfo_width()),
                                        random.randint(0, self.graph_canvas.winfo_height()))
            self.graph_canvas.add_line(textbox+"-L0", textbox+"-P0", textbox+"-P1")

    def shuffle_case_the_areas(self):
        for area in self.textbox_names:
            self.textbox_dict[area][0].set(random_capitalization_space_between(self.master.master.idutc_frame.kre8dict['use_id']))


def init_collage_areas(areas) -> dict:
    area_dict = {}
    for area in areas:
        area_dict[area] = []
    return area_dict


def random_capitalization_space_between(word: str) -> str:
    """Places a space between each letter and capitalizes random letters."""
    stamped_word = ""
    for letter in word:
        if random.random() >= 0.5:
            letter = letter.upper()
        stamped_word += letter + " "
    return stamped_word

