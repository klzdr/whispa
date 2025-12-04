import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

#helpers
def resource_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

def open_music_player():
    folder = os.path.join(os.path.dirname(__file__), "Whispa Music Player", "frontend")
    path = os.path.join(folder, "player.py")
    if os.path.exists(path):
        try:
            subprocess.Popen([sys.executable, path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Music Player:\n{e}")
    else:
        messagebox.showerror("Error", f"Music Player not found at:\n{path}")

def open_movie_player():
    folder = os.path.join(os.path.dirname(__file__), "Whispa Movie Player")
    path = os.path.join(folder, "main.py")
    if os.path.exists(path):
        try:
            subprocess.Popen([sys.executable, path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Movie Player:\n{e}")
    else:
        messagebox.showerror("Error", f"Movie Player not found at:\n{path}")

def open_tetris():
    folder = os.path.join(os.path.dirname(__file__), "Whispa Tetris")
    path = os.path.join(folder, "index.py")
    if os.path.exists(path):
        try:
            subprocess.Popen([sys.executable, path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Tetris:\n{e}")
    else:
        messagebox.showerror("Error", f"Tetris not found at:\n{path}")

class HomeWindow(tk.Tk):
    def __init__(self, username=None):
        super().__init__()
        self.username = username
        self.title("Whispa Home")
        self.geometry("500x400")
        self.configure(bg="#E8DEFF")
        self.resizable(False, False)

        self.main_frame = tk.Frame(self, bg="#E8DEFF")
        self.main_frame.pack(expand=True)

        if self.username:
            self.show_features()
        else:
            self.show_login_button()


    def show_login_button(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="Welcome to Whispa!",
            font=("Segoe UI", 16, "bold"),
            bg="#E8DEFF"
        ).pack(pady=30)

        tk.Button(
            self.main_frame,
            text="Log In",
            font=("Segoe UI", 14),
            width=20,
            height=2,
            command=self.go_to_login,
            bg="#6D33A7",
            fg="white"
        ).pack(pady=20)

    def go_to_login(self):
        self.withdraw()  # Hide home window
        login_path = os.path.join(os.path.dirname(__file__), "login.py")
        if os.path.exists(login_path):
            subprocess.Popen([sys.executable, login_path])
            self.destroy()  # Close home after login opens
        else:
            messagebox.showerror("Error", "Login window not found!")
            self.deiconify()  # Show home again if login.py missing

#after successful login
    def show_features(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text=f"Welcome, {self.username}!",
            font=("Segoe UI", 16, "bold"),
            bg="#E8DEFF"
        ).pack(pady=20)

        tk.Button(
            self.main_frame,
            text="Whispa Music Player",
            font=("Segoe UI", 14),
            width=25,
            height=2,
            command=open_music_player,
            bg="#6D33A7",
            fg="white"
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Whispa Movie Player",
            font=("Segoe UI", 14),
            width=25,
            height=2,
            command=open_movie_player,
            bg="#6D33A7",
            fg="white"
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Whispa Tetris",
            font=("Segoe UI", 14),
            width=25,
            height=2,
            command=open_tetris,
            bg="#6D33A7",
            fg="white"
        ).pack(pady=10)

#log out buttons
        tk.Button(
            self.main_frame,
            text="Log Out",
            font=("Segoe UI", 14),
            width=25,
            height=2,
            command=self.logout,
            bg="#6D33A7",
            fg="white"
        ).pack(pady=10)

        tk.Button(
            self.main_frame,
            text="Exit App",
            font=("Segoe UI", 14),
            width=25,
            height=2,
            command=self.quit,
            bg="#FF4D4D",
            fg="white"
        ).pack(pady=10)

    def logout(self):
        self.username = None
        self.show_login_button()


if __name__ == "__main__":
    username = None
    if len(sys.argv) > 1:
        username = sys.argv[1]

    app = HomeWindow(username)
    app.mainloop()
