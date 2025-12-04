import tkinter as tk
from tkinter import messagebox
from backend.database import get_user_by_username, create_user, verify_password
import subprocess
import sys
import os
import re

#style
BG = "#E8DEFF"
CARD = "#F3EFFF"
ACCENT = "#6D33A7"
TEXT = "#2B1550"

#root window
root = tk.Tk()
root.title("Whispa — Login")
root.geometry("520x600")
root.configure(bg=BG)
root.resizable(False, False)

try:
    from PIL import Image, ImageTk
    logo_img = Image.open(os.path.join(os.path.dirname(__file__), "Whispa.png"))
    logo_img = logo_img.resize((220, 48), Image.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(root, image=logo_photo, bg=BG)
    logo_label.image = logo_photo
    logo_label.pack(pady=(18, 6))
except Exception:
    tk.Label(root, text="Whispa", font=("Arial", 28, "bold"), fg=ACCENT, bg=BG).pack(pady=(24, 6))

card = tk.Frame(root, bg=CARD)
card.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=460, height=400)
tk.Label(card, text="Welcome to Whispa", font=("Segoe UI", 14, "bold"), fg=TEXT, bg=CARD).pack(pady=(12, 6))

# Pages dictionary
pages = {}
def show_page(name):
    for frame in pages.values():
        frame.place_forget()
    pages[name].place(x=20, y=60, width=420, height=400)

#password eye toggle
def toggle_password(entry, btn):
    if entry.cget("show") == "*":
        entry.config(show="")
        btn.config(text="👁")
    else:
        entry.config(show="*")
        btn.config(text="︵")

#login page
login_frame = tk.Frame(card, bg=CARD)
pages["login"] = login_frame

tk.Label(login_frame, text="Login", font=("Segoe UI", 12, "bold"), bg=CARD, fg=TEXT).pack(anchor="w", padx=6)

# Username
tk.Label(login_frame, text="Username", bg=CARD, fg=TEXT).pack(anchor="w", padx=6, pady=(8,0))
login_username = tk.Entry(login_frame, bd=1, relief=tk.FLAT)
login_username.pack(fill="x", padx=6, ipady=6)

# Password
tk.Label(login_frame, text="Password", bg=CARD, fg=TEXT).pack(anchor="w", padx=6, pady=(8,0))
pw_row = tk.Frame(login_frame, bg=CARD)
pw_row.pack(fill="x", padx=6)
login_password = tk.Entry(pw_row, bd=1, relief=tk.FLAT, show="*")
login_password.pack(side="left", fill="x", expand=True, ipady=6)

login_eye = tk.Button(pw_row, text="👁", bd=0, bg=CARD,
                      command=lambda: toggle_password(login_password, login_eye))
login_eye.pack(side="left", padx=(6,0))

# Login Action
def do_login(event=None):
    username = login_username.get().strip()
    password = login_password.get().strip()
    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password")
        return

    user = get_user_by_username(username)
    if user and verify_password(password, user[3], user[4]):
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()  # Close login window
        # Open home.py with username
        home_path = os.path.join(os.path.dirname(__file__), "home.py")
        subprocess.Popen([sys.executable, home_path, username])
    else:
        messagebox.showerror("Error", "Invalid username or password!")

# Buttons
action_row = tk.Frame(login_frame, bg=CARD)
action_row.pack(fill="x", padx=6, pady=(12,0))
tk.Button(action_row, text="Login", bg=ACCENT, fg="white", bd=0, command=do_login).pack(side="left", fill="x", expand=True, ipady=8)
tk.Button(action_row, text="Go to Signup", bg="#FFFFFF", fg=ACCENT, bd=0,
          command=lambda: show_page("signup")).pack(side="left", padx=(8,0), ipady=8)

login_username.bind("<Return>", do_login)
login_password.bind("<Return>", do_login)

#signup page
signup_frame = tk.Frame(card, bg=CARD)
pages["signup"] = signup_frame

tk.Label(signup_frame, text="Create Account", font=("Segoe UI", 12, "bold"), bg=CARD, fg=TEXT).pack(anchor="w", padx=6)

# Username
tk.Label(signup_frame, text="Username", bg=CARD, fg=TEXT).pack(anchor="w", padx=6, pady=(8,0))
signup_username = tk.Entry(signup_frame, bd=1, relief=tk.FLAT)
signup_username.pack(fill="x", padx=6, ipady=6)

# Email
tk.Label(signup_frame, text="Email", bg=CARD, fg=TEXT).pack(anchor="w", padx=6, pady=(8,0))
signup_email = tk.Entry(signup_frame, bd=1, relief=tk.FLAT)
signup_email.pack(fill="x", padx=6, ipady=6)

# Password
tk.Label(signup_frame, text="Password", bg=CARD, fg=TEXT).pack(anchor="w", padx=6, pady=(8,0))
spw_row = tk.Frame(signup_frame, bg=CARD)
spw_row.pack(fill="x", padx=6)
signup_password = tk.Entry(spw_row, bd=1, relief=tk.FLAT, show="*")
signup_password.pack(side="left", fill="x", expand=True, ipady=6)
signup_eye = tk.Button(spw_row, text="👁", bd=0, bg=CARD, command=lambda: toggle_password(signup_password, signup_eye))
signup_eye.pack(side="left", padx=(6,0))

# Confirm Password
tk.Label(signup_frame, text="Confirm Password", bg=CARD, fg=TEXT).pack(anchor="w", padx=6, pady=(8,0))
cpw_row = tk.Frame(signup_frame, bg=CARD)
cpw_row.pack(fill="x", padx=6)
signup_confirm = tk.Entry(cpw_row, bd=1, relief=tk.FLAT, show="*")
signup_confirm.pack(side="left", fill="x", expand=True, ipady=6)
signup_confirm_eye = tk.Button(cpw_row, text="👁", bd=0, bg=CARD, command=lambda: toggle_password(signup_confirm, signup_confirm_eye))
signup_confirm_eye.pack(side="left", padx=(6,0))

# Simple email validator
def valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Signup Action
def do_signup(event=None):
    username = signup_username.get().strip()
    email = signup_email.get().strip()
    pw = signup_password.get().strip()
    cpw = signup_confirm.get().strip()

    if not username or not email or not pw or not cpw:
        messagebox.showerror("Error", "Please fill all fields")
        return
    if not valid_email(email):
        messagebox.showerror("Error", "Enter a valid email")
        return
    if pw != cpw:
        messagebox.showerror("Error", "Passwords do not match")
        return
    if len(pw) < 6:
        messagebox.showerror("Error", "Password must be at least 6 characters")
        return

    try:
        create_user(username, email, pw)
        messagebox.showinfo("Success", "Account created! Please log in.")
        signup_username.delete(0, tk.END)
        signup_email.delete(0, tk.END)
        signup_password.delete(0, tk.END)
        signup_confirm.delete(0, tk.END)
        show_page("login")
    except Exception as e:
        messagebox.showerror("Error", f"Could not create account: {e}")

signup_row = tk.Frame(signup_frame, bg=CARD)
signup_row.pack(fill="x", padx=6, pady=(12,0))
tk.Button(signup_row, text="Create Account (Sign Up)", bg=ACCENT, fg="white", bd=0, command=do_signup).pack(side="left", fill="x", expand=True, ipady=8)
tk.Button(signup_row, text="Back to Login", bg="#FFFFFF", fg=ACCENT, bd=0,
          command=lambda: show_page("login")).pack(side="left", padx=(8,0), ipady=8)

signup_username.bind("<Return>", do_signup)
signup_email.bind("<Return>", do_signup)
signup_password.bind("<Return>", do_signup)
signup_confirm.bind("<Return>", do_signup)

show_page("login")

root.mainloop()
