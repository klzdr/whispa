# router.py
import tkinter as tk

class Router:
    def __init__(self, container, app):
        self.container = container
        self.app = app
        self.frames = {}

    def register(self, name, FrameClass):
        frame = FrameClass(self.container, self.app)
        self.frames[name] = frame
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show(self, name, params=None):
        frame = self.frames.get(name)
        if not frame:
            return
        # Hide navbar when showing player
        if hasattr(self.app, "nav"):
            if name == "player":
                try:
                    self.app.hide_navbar()
                except Exception:
                    pass
            else:
                try:
                    self.app.show_navbar()
                except Exception:
                    pass
        if hasattr(frame, "on_show"):
            frame.on_show(params or {})
        frame.tkraise()
