# ui_preview.py
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

NAV_BG = "#b8a1f2"  # navbar color
NAV_TEXT_ACCENT = "#5940B3"

class PreviewFrame(tk.Frame):
    CARD_W, CARD_H = 220, 330

    def __init__(self, parent, app):
        super().__init__(parent, bg="#c5b3f0")
        self.app = app
        self.movie = None

        # Layout: left poster, right info
        self.left = tk.Frame(self, bg="#c5b3f0")
        self.right = tk.Frame(self, bg="#c5b3f0")
        self.left.pack(side="left", fill="both", expand=False, padx=20, pady=20)
        self.right.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Poster frame
        self.poster_frame = tk.Frame(self.left, width=320, height=480, bg="#ddd")
        self.poster_frame.pack_propagate(False)
        self.poster_frame.pack(fill="both", expand=False)
        self.poster_lbl = tk.Label(self.poster_frame, bg="#dddddd")
        self.poster_lbl.pack(fill="both", expand=True)

        # Buttons
        btn_frame = tk.Frame(self.right, bg="#c5b3f0")
        btn_frame.pack(anchor="nw", pady=6)

        btn_config = {
            "bg": "#c5b3f0",
            "fg": NAV_TEXT_ACCENT,
            "bd": 0,
            "activebackground": "#c5b3f0",
            "font": ("Helvetica", 15, "bold"),
            "relief": "flat",
            "padx": 14,
            "pady": 14
        }

        self.play_btn = tk.Button(btn_frame, text="Play Trailer", command=self.play_trailer, **btn_config)
        self.play_btn.pack(side="left", padx=6)

        self.save_btn = tk.Button(btn_frame, text="Add to My List", command=self.add_to_list, **btn_config)
        self.save_btn.pack(side="left", padx=6)

        self.back_btn = tk.Button(btn_frame, text="Back", command=lambda: self.app.router.show("movies"), **btn_config)
        self.back_btn.pack(side="left", padx=6)

        # Info card
        self.info_card = tk.Frame(self.right, bg=NAV_BG, padx=20, pady=16)
        self.info_card.pack(anchor="nw", fill="x", pady=12)

        # Title
        self.title_lbl = tk.Label(
            self.info_card,
            text="",
            font=("Helvetica", 22, "bold"),
            fg=NAV_TEXT_ACCENT,
            bg=NAV_BG,
            anchor="w",
            justify="left",
            wraplength=500  # will be updated dynamically
        )
        self.title_lbl.pack(anchor="w", pady=(0,4))

        # Metadata
        self.metadata_lbl = tk.Label(
            self.info_card,
            text="",
            font=("Arial", 14),
            fg="white",
            bg=NAV_BG,
            justify="left",
            anchor="w",
            wraplength=500
        )
        self.metadata_lbl.pack(anchor="w", pady=(0,8))

        # Description
        self.desc_lbl = tk.Label(
            self.info_card,
            text="",
            font=("Arial", 14),
            fg="white",
            bg=NAV_BG,
            justify="left",
            anchor="w",
            wraplength=500
        )
        self.desc_lbl.pack(anchor="w")

        # Bind resize to dynamically update text width
        self.right.bind("<Configure>", self.update_wraplength)

    def update_wraplength(self, event=None):
        # calculate dynamic wraplength based on the right frame width minus some padding
        new_width = self.right.winfo_width() - 40
        if new_width > 100:  # minimum width
            self.title_lbl.config(wraplength=new_width)
            self.metadata_lbl.config(wraplength=new_width)
            self.desc_lbl.config(wraplength=new_width)

    def set_movie(self, movie):
        self.movie = movie

        # Title
        self.title_lbl.config(text=movie.get("title", "Untitled"))

        # Metadata
        cast = movie.get("cast", "Unknown")
        genre = movie.get("genre", "Unknown")
        duration = movie.get("duration", "Unknown")
        age = movie.get("age", "Unknown")
        metadata_text = f"Cast: {cast}\nGenre: {genre}\nDuration: {duration}\nAge: {age}"
        self.metadata_lbl.config(text=metadata_text)

        # Description
        self.desc_lbl.config(text=movie.get("description", "Description"))

        # Poster
        poster = movie.get("poster")
        if poster and os.path.exists(poster):
            try:
                im = Image.open(poster)
                target_w, target_h = 320, 480
                im_ratio = im.width / im.height
                target_ratio = target_w / target_h

                if im_ratio > target_ratio:
                    new_height = im.height
                    new_width = int(new_height * target_ratio)
                    left = (im.width - new_width) // 2
                    im = im.crop((left, 0, left + new_width, im.height))
                else:
                    new_width = im.width
                    new_height = int(new_width / target_ratio)
                    top = (im.height - new_height) // 2
                    im = im.crop((0, top, im.width, top + new_height))

                im = im.resize((target_w, target_h), Image.LANCZOS)
                self._poster_img = ImageTk.PhotoImage(im)
                self.poster_lbl.config(image=self._poster_img, text="")
            except Exception:
                self.poster_lbl.config(text="[poster error]")
        else:
            self.poster_lbl.config(text="[no poster]")

    def play_trailer(self):
        if not self.movie:
            return
        if self.movie.get("trailer"):
            self.app.router.show("player")
            player = self.app.router.frames.get("player")
            if hasattr(player, "set_movie"):
                player.set_movie(self.movie)
        else:
            messagebox.showinfo("No trailer", "No trailer file found for this movie.")

    def add_to_list(self):
        if not self.movie:
            return
        sid = self.movie["id"]
        if sid not in self.app.state["saved"]:
            self.app.state["saved"].append(sid)
            messagebox.showinfo("Added", f"\"{self.movie['title']}\" added to My List.")
        else:
            messagebox.showinfo("Already saved", f"\"{self.movie['title']}\" is already in My List.")
