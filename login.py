import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import subprocess
import sys
import sqlite3


# ==========================
# Login Function
# ==========================
def login():

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username.get(), password.get())
    )

    user = cursor.fetchone()
    conn.close()

    if user:

        messagebox.showinfo(
            "Success",
            "Login Successful"
        )

        root.destroy()

        subprocess.Popen(
            [sys.executable, "splash.py"]
        )

    else:

        messagebox.showerror(
            "Error",
            "Invalid Username or Password"
        )


# ==========================
# Forgot Password
# ==========================
def forgot_password():

    uname = simpledialog.askstring(
        "Forgot Password",
        "Enter Username"
    )

    if not uname:
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        (uname,)
    )

    user = cursor.fetchone()

    if not user:

        messagebox.showerror(
            "Error",
            "Username Not Found"
        )

        conn.close()
        return

    new_pass = simpledialog.askstring(
        "New Password",
        "Enter New Password",
        show="*"
    )

    if not new_pass:
        conn.close()
        return

    confirm = simpledialog.askstring(
        "Confirm Password",
        "Confirm New Password",
        show="*"
    )

    if new_pass != confirm:

        messagebox.showerror(
            "Error",
            "Passwords Do Not Match"
        )

        conn.close()
        return

    cursor.execute(
        "UPDATE users SET password=? WHERE username=?",
        (new_pass, uname)
    )

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Password Changed Successfully"
    )


# ==========================
# Show Password
# ==========================
show = False

def toggle():

    global show

    show = not show

    password.config(
        show="" if show else "*"
    )
    # ==========================
# Login Window
# ==========================

root = tk.Tk()
root.title("AI Smart Attendance System - Login")
root.geometry("500x600")
root.configure(bg="white")
root.resizable(False, False)

# Center Window
w, h = 500, 600
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws - w) // 2
y = (hs - h) // 2
root.geometry(f"{w}x{h}+{x}+{y}")

# ==========================
# College Logo
# ==========================

img = Image.open("assets/college_logo.png")
img = img.resize((180, 180))

logo = ImageTk.PhotoImage(img)

tk.Label(
    root,
    image=logo,
    bg="white"
).pack(pady=10)

# ==========================
# Heading
# ==========================

tk.Label(
    root,
    text="UNITED INSTITUTE OF TECHNOLOGY",
    font=("Arial",18,"bold"),
    fg="#003366",
    bg="white"
).pack()

tk.Label(
    root,
    text="AI SMART ATTENDANCE SYSTEM",
    font=("Arial",14,"bold"),
    fg="green",
    bg="white"
).pack(pady=10)

# ==========================
# Username
# ==========================

tk.Label(
    root,
    text="Username",
    bg="white",
    font=("Arial",12)
).pack()

username = tk.Entry(
    root,
    font=("Arial",12),
    width=30
)

username.pack(pady=5)

# ==========================
# Password
# ==========================

tk.Label(
    root,
    text="Password",
    bg="white",
    font=("Arial",12)
).pack()

password = tk.Entry(
    root,
    font=("Arial",12),
    width=30,
    show="*"
)

password.pack(pady=5)

# ==========================
# Show Password Button
# ==========================

tk.Button(
    root,
    text="👁 Show / Hide Password",
    command=toggle,
    bg="#2196F3",
    fg="white",
    width=22
).pack(pady=8)
# ==========================
# LOGIN Button
# ==========================

tk.Button(
    root,
    text="LOGIN",
    bg="green",
    fg="white",
    font=("Arial",14,"bold"),
    width=20,
    command=login
).pack(pady=10)

# ==========================
# Forgot Password Button
# ==========================

tk.Button(
    root,
    text="Forgot Password",
    bg="orange",
    fg="white",
    font=("Arial",11,"bold"),
    width=20,
    command=forgot_password
).pack(pady=5)

# ==========================
# Exit Button
# ==========================

tk.Button(
    root,
    text="Exit",
    bg="red",
    fg="white",
    font=("Arial",11,"bold"),
    width=20,
    command=root.destroy
).pack(pady=5)

# ==========================
# Enter Key Login
# ==========================

root.bind("<Return>", lambda e: login())

# ==========================
# Footer
# ==========================

tk.Label(
    root,
    text="Developed By : Anmol Ojha\nAI Smart Attendance System",
    font=("Arial",10,"italic"),
    fg="gray",
    bg="white"
).pack(side="bottom", pady=15)

# ==========================
# Run Window
# ==========================

root.mainloop()