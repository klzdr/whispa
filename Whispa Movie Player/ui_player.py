import tkinter as tk
from tkinter import ttk, messagebox
import vlc
import os
import platform

PRIMARY = "#b8a1f2"
WINDOW_BG = "#c5b3f0"
CONTROL_BG = "#222"
VIDEO_BG = "#000"

class PlayerFrame(tk.Frame):
    def __init__(self, parent, app, video=None):
        super().__init__(parent, bg=WINDOW_BG)
        self.app = app
        self.video_path = video
        self.instance = vlc.Instance('--no-video-title-show', '--quiet', '--avcodec-hw=none')
        self.player = self.instance.media_player_new()

        # Hide top navbar
        self.app.hide_navbar()

        # Video display
        self.video_panel = tk.Frame(self, bg=VIDEO_BG, height=480)
        self.video_panel.pack(fill="both", expand=True, padx=12, pady=6)
        self.video_panel.pack_propagate(False)

        # Bottom control bar
        self.bar = tk.Frame(self, bg=CONTROL_BG, height=60)
        self.bar.pack(fill="x", side="bottom")
        self.bar.pack_propagate(False)

        # Back button + title
        left = tk.Frame(self.bar, bg=CONTROL_BG)
        left.pack(side="left", padx=8)
        self.back_btn = ttk.Button(left, text="← Back", command=self.go_back)
        self.back_btn.pack(side="left", padx=6)
        self.title_lbl = tk.Label(left, text="", font=("Helvetica", 14, "bold"), bg=CONTROL_BG, fg="#fff")
        self.title_lbl.pack(side="left", padx=6)

        # Play/pause + skip
        self.is_playing = False
        ttk.Button(left, text="<< 10s", command=lambda: self.skip(-10)).pack(side="left", padx=6)
        self.play_btn = ttk.Button(left, text="Play", command=self.toggle_play)
        self.play_btn.pack(side="left", padx=6)
        ttk.Button(left, text="10s >>", command=lambda: self.skip(10)).pack(side="left", padx=6)

        # Center: progress
        center = tk.Frame(self.bar, bg=CONTROL_BG)
        center.pack(side="left", fill="both", expand=True, padx=6)
        self.time_label = tk.Label(center, text="00:00", bg=CONTROL_BG, fg="#fff")
        self.time_label.pack(side="left", padx=6)
        self.scale = ttk.Scale(center, from_=0, to=1000, orient="horizontal", command=self.on_scale_move)
        self.scale.pack(side="left", fill="x", expand=True, padx=6, pady=12)
        self.total_label = tk.Label(center, text="00:00", bg=CONTROL_BG, fg="#fff")
        self.total_label.pack(side="left", padx=6)

        # Volume + fullscreen
        right = tk.Frame(self.bar, bg=CONTROL_BG)
        right.pack(side="right", padx=8)
        self.volume_var = tk.DoubleVar(value=100)
        ttk.Scale(right, from_=0, to=100, orient="horizontal", variable=self.volume_var,
                  command=self.on_volume_change, length=100).pack(side="left", padx=6, pady=10)
        self.full_btn = ttk.Button(right, text="Fullscreen", command=self.toggle_fullscreen)
        self.full_btn.pack(side="left", padx=6, pady=8)

        # Seek dragging
        self.is_dragging = False
        self.scale.bind("<Button-1>", self.start_drag)
        self.scale.bind("<ButtonRelease-1>", self.end_drag)

        # Window handle
        self.after(120, self._attach_video_handle)

        # Update loop
        self.after(200, self.update_progress_loop)

        # fullscreen flag
        self.is_fullscreen = False

        if video:
            self.load_media(video)

    # ----------------------
    # Navigation
    # ----------------------
    def go_back(self):
        try:
            self.player.pause()
        except Exception:
            pass
        self.app.show_navbar()
        self.app.router.show("movies")

    # ----------------------
    # Video
    # ----------------------
    def _attach_video_handle(self):
        wid = self.video_panel.winfo_id()
        sys_plat = platform.system()
        try:
            if sys_plat == "Windows":
                self.player.set_hwnd(wid)
            elif sys_plat == "Linux":
                self.player.set_xwindow(wid)
            elif sys_plat == "Darwin":
                try:
                    self.player.set_nsobject(wid)
                except Exception:
                    pass
        except Exception:
            pass

    def load_media(self, path):
        if not path or not os.path.exists(path):
            messagebox.showerror("Missing file", "Trailer file not found.")
            return
        self.video_path = os.path.abspath(path)
        media = self.instance.media_new(self.video_path)
        self.player.set_media(media)
        title = os.path.splitext(os.path.basename(path))[0]
        self.title_lbl.config(text=self.app.state["movies"][0]["title"] if self.app.state["movies"] else title)
        self.player.play()
        self.player.audio_set_volume(int(self.volume_var.get()))
        self.is_playing = True
        self.play_btn.config(text="Pause")

    def set_movie(self, movie):
        trailer = movie.get("trailer")
        if not trailer or not os.path.exists(trailer):
            messagebox.showinfo("No trailer", "No trailer file found for this movie.")
            return
        self.load_media(trailer)
        self.title_lbl.config(text=movie.get("title", "Unknown"))

    # ----------------------
    # Controls
    # ----------------------
    def toggle_play(self):
        try:
            state = self.player.get_state()
            if state == vlc.State.Playing:
                self.player.pause()
                self.is_playing = False
                self.play_btn.config(text="Play")
            else:
                self.player.play()
                self.is_playing = True
                self.play_btn.config(text="Pause")
        except Exception:
            pass

    def skip(self, seconds):
        try:
            length = self.player.get_length() / 1000.0
            if length <= 0: return
            pos = self.player.get_position() * length
            new = max(0, min(length, pos + seconds))
            self.player.set_time(int(new * 1000))
        except Exception:
            pass

    def on_volume_change(self, val):
        try:
            self.player.audio_set_volume(int(float(val)))
        except Exception:
            pass

    # ----------------------
    # Seek
    # ----------------------
    def start_drag(self, ev):
        self.is_dragging = True

    def on_scale_move(self, value):
        try:
            frac = float(value) / 1000.0
        except Exception:
            frac = 0.0
        length_ms = self.player.get_length()
        if length_ms > 0:
            sec = int(frac * (length_ms / 1000.0))
            self.time_label.config(text=self._format_time(sec))

    def end_drag(self, ev):
        try:
            frac = self.scale.get() / 1000.0
            self.player.set_position(frac)
        except Exception:
            pass
        self.is_dragging = False

    # ----------------------
    # Fullscreen
    # ----------------------
    def toggle_fullscreen(self):
        root = self.winfo_toplevel()
        self.is_fullscreen = not self.is_fullscreen
        root.attributes("-fullscreen", self.is_fullscreen)

    # ----------------------
    # Update loop
    # ----------------------
    def update_progress_loop(self):
        try:
            length_ms = self.player.get_length()
            if length_ms > 0:
                total_secs = int(length_ms / 1000)
                self.total_label.config(text=self._format_time(total_secs))
                if not self.is_dragging:
                    pos = self.player.get_position()
                    if pos is None or pos < 0:
                        pos = 0.0
                    self.scale.set(pos * 1000)
                    cur = int(pos * total_secs)
                    self.time_label.config(text=self._format_time(cur))
            else:
                self.total_label.config(text="00:00")
                if not self.is_dragging:
                    self.scale.set(0)
                    self.time_label.config(text="00:00")
        except Exception:
            pass
        self.after(150, self.update_progress_loop)

    def _format_time(self, seconds):
        m = seconds // 60
        s = seconds % 60
        return f"{int(m):02d}:{int(s):02d}"
