import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageDraw, ImageTk
import pygame
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(current_dir)

pygame.mixer.init()

#PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_FOLDER = os.path.join(BASE_DIR, "..", "music")
COVER_FOLDER = os.path.join(BASE_DIR, "..", "covers")

# Default Images
DEFAULT_COVER_FILENAME = "image_773db5.png"  # fallback cover image
DEFAULT_COVER_PATH = os.path.join(COVER_FOLDER, DEFAULT_COVER_FILENAME)
USER_ICON_PATH = os.path.join(BASE_DIR, "user_icon.png")

# Global State
USER_FAVORITES = []
is_playing = False
is_seeking = False
current_index = 0
current_cover_photo = None
user_icon_photo = None
heart_icon_photo = None
heart_filled_photo = None
song_length = 0
update_timer_id = None
current_offset = 0

if not os.path.exists(COVER_FOLDER):
    os.makedirs(COVER_FOLDER)

songs = [f for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]

#FUNCTIONS
def load_cover_art(song_name):
    global current_cover_photo
    if not song_name:
        cover_label.config(image='', text="Pick a Song")
        return
    base_name = os.path.splitext(song_name)[0]
    cover_filename = base_name + ".png"
    cover_path = os.path.join(COVER_FOLDER, cover_filename)
    if not os.path.exists(cover_path):
        cover_path = DEFAULT_COVER_PATH

    try:
        img = Image.open(cover_path).resize((200, 200), Image.LANCZOS)
        current_cover_photo = ImageTk.PhotoImage(img)
        cover_label.config(image=current_cover_photo, text="")
        cover_label.image = current_cover_photo
    except Exception as e:
        print(f"Error loading cover art: {e}")
        cover_label.config(image='', text="Pick a Song")


def update_favorites_button():
    if not songs:
        return
    current_song_name = songs[current_index]
    if current_song_name in USER_FAVORITES:
        favorites_btn.config(image=heart_filled_photo)
    else:
        favorites_btn.config(image=heart_icon_photo)


def update_play_pause_button():
    if is_playing:
        play_pause_btn.config(text="Pause")
    else:
        play_pause_btn.config(text="Play")

#CONTROL FUNCTIONS
def play_song():
    global current_index, is_playing, song_length, current_offset
    if not songs:
        song_title_label.config(text="No songs found in music folder.")
        return

    current_song_name = songs[current_index]
    full_path = os.path.join(MUSIC_FOLDER, current_song_name)

    pygame.mixer.music.load(full_path)
    pygame.mixer.music.play()
    current_offset = 0
    song_length = pygame.mixer.Sound(full_path).get_length()
    slider.config(to=song_length)

    song_title_label.config(text=current_song_name)
    load_cover_art(current_song_name)
    is_playing = True
    favorites_btn.pack(side=tk.LEFT)  # Show favorites button only when a song plays
    update_play_pause_button()
    update_favorites_button()
    update_slider()


def toggle_play_pause():
    global is_playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        is_playing = False
    elif pygame.mixer.music.get_pos() > 0:
        pygame.mixer.music.unpause()
        is_playing = True
    else:
        play_song()
        is_playing = True
    update_play_pause_button()


def stop_song():
    global is_playing
    pygame.mixer.music.stop()
    is_playing = False
    update_play_pause_button()
    slider.set(0)


def next_song():
    global current_index
    stop_song()
    current_index = (current_index + 1) % len(songs)
    play_song()


def prev_song():
    global current_index
    stop_song()
    current_index = (current_index - 1 + len(songs)) % len(songs)
    play_song()


def toggle_favorite():
    global USER_FAVORITES
    if not songs:
        return
    current_song_name = songs[current_index]
    if current_song_name in USER_FAVORITES:
        USER_FAVORITES.remove(current_song_name)
        messagebox.showinfo("Favorites", f"Removed '{current_song_name}' from favorites.")
    else:
        USER_FAVORITES.append(current_song_name)
        messagebox.showinfo("Favorites", f"Added '{current_song_name}' to favorites.")
    update_favorites_button()


def select_song(event):
    global current_index
    selected = playlist_box.curselection()
    if selected:
        stop_song()
        current_index = selected[0]
        play_song()


#SLIDER FUNCTIONS
def slider_press(event):
    global is_seeking, update_timer_id
    is_seeking = True
    if update_timer_id:
        root.after_cancel(update_timer_id)
        update_timer_id = None


def slider_release(event):
    global is_seeking, is_playing, current_offset
    if not songs: return
    new_pos = slider.get()
    current_song = os.path.join(MUSIC_FOLDER, songs[current_index])
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play(start=new_pos)
        current_offset = new_pos
        is_playing = True
        update_play_pause_button()
        slider.set(new_pos)
    except Exception as e:
        print(f"Error seeking: {e}")
    is_seeking = False
    update_slider()


def update_slider():
    global is_seeking, update_timer_id, current_offset
    update_timer_id = root.after(100, update_slider)
    if is_seeking: return
    if pygame.mixer.music.get_busy() and song_length > 0:
        current_time = pygame.mixer.music.get_pos() / 1000 + current_offset
        if abs(slider.get() - current_time) > 0.1:
            slider.set(current_time)
        if is_playing and current_time >= song_length - 0.1:
            next_song()


#MENU FUNCTIONS
def show_favorites():
    fav_window = tk.Toplevel(root)
    fav_window.title("My Favorites")
    fav_window.geometry("300x400")
    fav_window.configure(bg="#D3C3F5")
    tk.Label(fav_window, text="Favorite Songs", font=("Arial", 14, "bold"), bg="#D3C3F5").pack(pady=10)
    fav_listbox = tk.Listbox(fav_window, width=40, height=15)
    if not USER_FAVORITES:
        fav_listbox.insert(tk.END, "No favorites added yet.")
    else:
        for song in USER_FAVORITES:
            fav_listbox.insert(tk.END, song)
    fav_listbox.pack(padx=10, pady=5)


def logout():
    stop_song()
    root.destroy()
    login_path = os.path.join(BASE_DIR, "login.py")
    os.system(f'py "{login_path}"')


#GUI
root = tk.Tk()
root.title("Whispa")
root.geometry("800x500")
root.configure(bg="#C5B3F0")

# Load images
try:
    logo_img = Image.open(os.path.join(BASE_DIR, "Whispa.png")).resize((100,50), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)

    user_img = Image.open(USER_ICON_PATH).resize((30,30), Image.LANCZOS)
    user_icon_photo = ImageTk.PhotoImage(user_img)

    icon_size = (30,30)
    heart_empty_file = os.path.join(BASE_DIR, "heart_empty.png")
    heart_filled_file = os.path.join(BASE_DIR, "heart_filled.png")
    heart_icon_photo = ImageTk.PhotoImage(Image.open(heart_empty_file).resize(icon_size, Image.LANCZOS))
    heart_filled_photo = ImageTk.PhotoImage(Image.open(heart_filled_file).resize(icon_size, Image.LANCZOS))
except Exception as e:
    print(f"Error loading images: {e}")
    logo_photo = None
    user_icon_photo = None
    heart_icon_photo = None
    heart_filled_photo = None

# Top bar
top_bar = tk.Frame(root, bg="#B8A1F2", height=60)
top_bar.pack(side=tk.TOP, fill=tk.X)
tk.Label(top_bar, image=logo_photo, bg="#B8A1F2").pack(side=tk.LEFT, padx=10)

favorites_btn_top = tk.Button(top_bar, text="Favorites", command=show_favorites, bg="#B8A1F2", bd=0, fg="#111")
favorites_btn_top.pack(side=tk.RIGHT, padx=10, pady=12)

back_btn_top = tk.Button(top_bar, text="Back to Home", command=root.destroy, bg="#B8A1F2", bd=0, fg="#111")
back_btn_top.pack(side=tk.RIGHT, padx=10, pady=12)

# Main content
main_frame = tk.Frame(root, bg="#C5B3F0")
main_frame.pack(fill=tk.BOTH, expand=True)

# Playlist
playlist_frame = tk.Frame(main_frame, bg="#C5B3F0", width=250)
playlist_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
tk.Label(playlist_frame, text="Playlist", font=("Arial", 14, "bold"), bg="#C5B3F0").pack(pady=5)
playlist_box = tk.Listbox(playlist_frame)
for s in songs:
    playlist_box.insert(tk.END, s)
playlist_box.pack(fill=tk.Y, expand=True)
playlist_box.bind("<<ListboxSelect>>", select_song)

# Player panel
player_frame = tk.Frame(main_frame, bg="#D3C3F5")
player_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Song title and favorites
title_row = tk.Frame(player_frame, bg="#D3C3F5")
title_row.pack(pady=10)
song_title_label = tk.Label(title_row, text="Select a Song", font=("Arial", 16, "bold"), bg="#D3C3F5")
song_title_label.pack(side=tk.LEFT, padx=(0,10))

# Favorites button (initially hidden)
favorites_btn = tk.Button(title_row, image=heart_icon_photo, command=toggle_favorite, bd=0, bg="#D3C3F5")
favorites_btn.pack(side=tk.LEFT)
favorites_btn.pack_forget()

# Cover art
cover_frame = tk.Frame(player_frame, width=200, height=200, bg="#9B78F0")
cover_frame.pack(pady=10)
cover_label = tk.Label(cover_frame, bg="#9B78F0", width=200, height=200, text="Loading Cover...")
cover_label.pack(fill=tk.BOTH, expand=True)
load_cover_art("")

# Slider
slider = ttk.Scale(player_frame, from_=0, to=100, orient=tk.HORIZONTAL)
slider.pack(fill=tk.X, padx=20, pady=10)
slider.bind("<ButtonPress-1>", slider_press)
slider.bind("<ButtonRelease-1>", slider_release)

# Controls
controls_frame = tk.Frame(player_frame, bg="#D3C3F5")
controls_frame.pack(pady=10)
tk.Button(controls_frame, text="Prev", width=8, command=prev_song).grid(row=0, column=0, padx=5)
play_pause_btn = tk.Button(controls_frame, text="Play", width=8, command=toggle_play_pause)
play_pause_btn.grid(row=0, column=1, padx=5)
tk.Button(controls_frame, text="Next", width=8, command=next_song).grid(row=0, column=2, padx=5)

# Start GUI loop
update_slider()
root.mainloop()
