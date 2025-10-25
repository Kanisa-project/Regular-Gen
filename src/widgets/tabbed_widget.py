from src.widgets.basik_widget import BasikWidget

class TabbedWidget(BasikWidget):
    def __init__(self, width, height, master=None, text="Tabbed"):
        super().__init__(width, height, master, text)