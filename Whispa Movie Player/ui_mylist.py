import tkinter as tk
from tkinter import ttk
from components.movie_card import MovieCard

class MyListFrame(tk.Frame):
    COLS = 6
    CARD_W = 220
    CARD_H = 330
    PADDING = 16

    def __init__(self, parent, app):
        super().__init__(parent, bg="#c5b3f0")
        self.app = app
        self.cards = []

        title = tk.Label(self, text="My List", font=("Arial", 20, "bold"), bg="#c5b3f0", fg="#5940B3")
        title.pack(anchor="nw", padx=20, pady=10)

        self.canvas = tk.Canvas(self, bg="#c5b3f0", highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.vscroll.pack(side="right", fill="y")

        self.inner = tk.Frame(self.canvas, bg="#c5b3f0")
        self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def refresh(self):
        for c in self.cards:
            c.destroy()
        self.cards = []

        saved_ids = set(self.app.state.get("saved", []))
        movies = [m for m in self.app.state["movies"] if m["id"] in saved_ids]

        for idx, m in enumerate(movies):
            card = MovieCard(
                self.inner,
                m,
                click_callback=self.open_preview,
                card_width=self.CARD_W,
                card_height=self.CARD_H,
                bg="#c5b3f0"
            )
            row = idx // self.COLS
            col = idx % self.COLS
            card.grid(row=row, column=col, padx=self.PADDING//2, pady=self.PADDING//2)

    def open_preview(self, movie):
        self.app.router.show("preview")
        prev = self.app.router.frames.get("preview")
        if hasattr(prev, "set_movie"):
            prev.set_movie(movie)

    def on_show(self, params=None):
        self.refresh()
