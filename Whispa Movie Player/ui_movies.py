import tkinter as tk
from tkinter import ttk
from components.movie_card import MovieCard

class MoviesFrame(tk.Frame):
    CARD_W = 220
    CARD_H = 330
    PADDING = 16
    FIXED_COLS = 6   # ← changed to 6 columns

    def __init__(self, parent, app):
        super().__init__(parent, bg="#c5b3f0")
        self.app = app
        self.cards = []
        self.current_filter = None

        # Canvas + scrollbar
        self.canvas = tk.Canvas(self, bg="#c5b3f0", highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vscroll.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.vscroll.pack(side="right", fill="y")

        # Inner content
        self.inner = tk.Frame(self.canvas, bg="#c5b3f0")
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.reflow())

        self.build_cards(self.app.state["movies"])

    def build_cards(self, movies):
        for c in self.cards:
            c.destroy()
        self.cards = []

        for m in movies:
            card = MovieCard(
                self.inner,
                m,
                click_callback=self.open_preview,
                card_width=self.CARD_W,
                card_height=self.CARD_H,
                bg="#c5b3f0"
            )
            self.cards.append(card)

        self.reflow()

    def reflow(self):
        canvas_width = self.canvas.winfo_width()
        cols = self.FIXED_COLS
        col_width = self.CARD_W + self.PADDING

        total_width = cols * col_width
        offset_x = max(0, (canvas_width - total_width) // 2)

        try:
            self.canvas.coords(self.window_id, offset_x, 20)
        except:
            pass

        for idx, card in enumerate(self.cards):
            r = idx // cols
            c = idx % cols
            card.grid(row=r, column=c, padx=self.PADDING//2, pady=self.PADDING//2, sticky="n")

        for c in range(cols):
            self.inner.grid_columnconfigure(c, weight=0, minsize=self.CARD_W + self.PADDING)

    def open_preview(self, movie):
        self.app.router.show("preview")
        preview = self.app.router.frames.get("preview")
        if hasattr(preview, "set_movie"):
            preview.set_movie(movie)

    def on_show(self, params=None):
        if params and params.get("filter"):
            movies = params["filter"]
        else:
            movies = self.app.state["movies"]

        self.build_cards(movies)
