import os
import tkinter as tk
from PIL import Image, ImageTk

class MovieCard(tk.Frame):
    """
    Movie card shows a poster that COVER-fills the card area (cropped if needed),
    centers the image horizontally & vertically, and has a click handler.
    Titles are not shown on the card (per request).
    """
    def __init__(self, parent, movie, click_callback, card_width=160, card_height=240, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.movie = movie
        self.click_callback = click_callback
        self.card_w = card_width
        self.card_h = card_height
        # keep a neutral bg so if poster has transparency it shows nicely
        self.config(bg="#c5b3f0", bd=0, highlightthickness=0, width=self.card_w, height=self.card_h)
        self.pack_propagate(False)

        # image area as fixed frame so label doesn't stretch the layout
        self.img_frame = tk.Frame(self, width=self.card_w, height=self.card_h, bg="#222")
        self.img_frame.pack_propagate(False)
        self.img_frame.pack(fill="both", expand=True)

        self.img_lbl = tk.Label(self.img_frame, bg="#222")
        self.img_lbl.place(relx=0.5, rely=0.5, anchor="center")  # center the label in the frame

        self._img = None  # PhotoImage ref

        self.load_image()

        # click binding to whole card
        for w in (self.img_lbl, self.img_frame, self):
            w.bind("<Button-1>", self._on_click)

    def load_image(self):
        poster = self.movie.get("poster")
        if poster and os.path.exists(poster):
            try:
                im = Image.open(poster).convert("RGB")
                target_w, target_h = self.card_w, self.card_h

                # COVER logic: scale to fully cover and crop center
                img_ratio = im.width / im.height
                target_ratio = target_w / target_h

                if img_ratio > target_ratio:
                    # image is wider than target -> fit height then crop width
                    scale = target_h / im.height
                    new_h = target_h
                    new_w = int(im.width * scale)
                else:
                    # image is taller (or equal) -> fit width then crop height
                    scale = target_w / im.width
                    new_w = target_w
                    new_h = int(im.height * scale)

                resized = im.resize((new_w, new_h), Image.LANCZOS)

                # center-crop
                left = max(0, (new_w - target_w) // 2)
                top = max(0, (new_h - target_h) // 2)
                right = left + target_w
                bottom = top + target_h
                cropped = resized.crop((left, top, right, bottom))

                self._img = ImageTk.PhotoImage(cropped)
                self.img_lbl.config(image=self._img, text="")
                # ensure label size
                self.img_lbl.config(width=target_w, height=target_h)
            except Exception as e:
                # fallback
                self.img_lbl.config(text="[image error]", bg="#ddd")
        else:
            self.img_lbl.config(text="[no image]", bg="#ddd")

    def _on_click(self, event=None):
        if callable(self.click_callback):
            self.click_callback(self.movie)
