# Python
# src/app/main_window.py
import tkinter as tk
from src.app.wiring import build_application
from src.services.logging import setup_logging

def run_app():
    setup_logging()
    root = tk.Tk()
    root.title("kanisaGen")
    root.configure(background="#0f6faa")
    root.wm_attributes("-fullscreen", 'True')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    app = build_application(root, screen_width, screen_height)
    app.mainloop()