from src.utils import ast_visitor
import basik_widget


class Graphter(basik_widget.BasikWidget):
    def __init__(self, width, height, master=None):
        super().__init__(master=master, width=width, height=height)
        self.setup_text_boxes({"file_name": "idutc.py"})
        self.setup_button_choices(["Hexagon", "Shell", "Circular"])

        self.button_dict['Hexagon'][1].config(command=self.hexagon_parsing)
        self.button_dict['Shell'][1].config(command=self.shell_parsing)
        self.button_dict['Circular'][1].config(command=self.circular_parsing)

        self.kanisa_visitor = ast_visitor.kanisaVisitor()

    def hexagon_parsing(self):
        ast_visitor.draw_hexagon_graph(self.textbox_dict['file_name'][0].get())

    def circular_parsing(self):
        ast_visitor.draw_circular_graph(self.textbox_dict['file_name'][0].get())

    def shell_parsing(self):
        ast_visitor.draw_shell_graph(self.textbox_dict['file_name'][0].get())
