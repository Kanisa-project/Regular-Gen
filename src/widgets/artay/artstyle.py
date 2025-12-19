from src.settings import themery as t
from src.widgets.tabbed_widget import TabbedWidget


class Artyle(TabbedWidget):
    def __init__(self, width, height, master=None):
        """
        Base art style tab that has buttons, sliders, checkboxes and dropdown menus for choosing options from within
        a glyth, glyph, categories, sprite, gaim, mujic, fotoes and any other forms of art style.

        :param width:
        :param height:
        :param master:
        :param idutc:
        :param texioty:
        """
        super(Artyle, self).__init__(master=master, width=width, height=height)
        self.tab_name = "Basic"

    def update_slider_label(self) -> str:
        return str(self.widget_display_array)

    def set_artributes(self, kre8dict: dict) -> dict:
        selected_colors = []
        artribute_dict = {}

        if "Door" in kre8dict["artributes"]:
            artribute_dict["transparency"] = 0.85
        elif "Window" in kre8dict["artributes"]:
            artribute_dict["transparency"] = 0.35

        if "Rainbow" in kre8dict["artributes"]:
            for ltr in kre8dict["use_id"]:
                if ltr.lower() in t.ALPHANUMERIC_COLORS:
                    selected_colors.append(t.ALPHANUMERIC_COLORS[ltr.lower()])
                else:
                    selected_colors.append(t.PUNCTUATION_COLORS[ltr.lower()])
        elif "Cloud" in kre8dict["artributes"]:
            shadelvl = 255 // len(kre8dict["use_id"])
            selected_colors.append((0, 0, 0))
            for i in range(len(kre8dict["use_id"])-2):
                selected_colors.append(((i + 1) * shadelvl, (i + 1) * shadelvl, (i + 1) * shadelvl))
            selected_colors.append((255, 255, 255))
        # print("ARTYLECOLORS: ", kre8dict)
        artribute_dict['colors'] = selected_colors

        if "Chicken" in kre8dict["artributes"]:
            artribute_dict['size_scale'] = 0.2
        elif "Dog" in kre8dict["artributes"]:
            artribute_dict['size_scale'] = 0.4
        elif "Camel" in kre8dict["artributes"]:
            artribute_dict['size_scale'] = 0.8

        if "Pen" in kre8dict["artributes"]:
            artribute_dict["accuracy"] = kre8dict["number_list"][:3]
        elif "Crayon" in kre8dict["artributes"]:
            artribute_dict["accuracy"] = kre8dict["number_list"][3:]

        return artribute_dict
