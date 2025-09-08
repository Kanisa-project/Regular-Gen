# Python
# src/app/wiring.py
from main import Application  # Create this when you move the Application widget

def build_application(root, screen_w: int, screen_h: int):
    # In future: construct services, pass into widgets, assemble Application
    app = Application(master=root, screen_w=screen_w, screen_h=screen_h)
    return app