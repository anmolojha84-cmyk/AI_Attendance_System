import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import sys

root = tk.Tk()

root.title("Loading...")
root.geometry("500x400")
root.configure(bg="white")
root.overrideredirect(True)

# Center Window
w = 500
h = 400

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

x = (ws - w) // 2
y = (hs - h) // 2

root.geometry(f"{w}x{h}+{x}+{y}")

# Logo
try:
    img = Image.open("assets/college_logo.png")
    img = img.resize((120,120))
    logo = ImageTk.PhotoImage(img)

    tk.Label(root, image=logo, bg="white").pack(pady=15)
except:
    pass

tk.Label(
    root,
    text="UNITED INSTITUTE OF TECHNOLOGY",
    font=("Arial",18,"bold"),
    bg="white",
    fg="#003366"
).pack()

tk.Label(
    root,
    text="AI SMART ATTENDANCE SYSTEM",
    font=("Arial",14,"bold"),
    bg="white",
    fg="green"
).pack(pady=10)

progress = ttk.Progressbar(
    root,
    orient="horizontal",
    length=350,
    mode="determinate"
)

progress.pack(pady=20)

loading = tk.Label(
    root,
    text="Loading...",
    bg="white",
    font=("Arial",11)
)

loading.pack()

value = 0

def load():
    global value

    if value < 100:
        value += 2
        progress["value"] = value
        root.after(40, load)
    else:
        root.destroy()
        subprocess.Popen([sys.executable, "gui.py"])

load()

root.mainloop()