import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import subprocess
import sys
import os
import csv
from datetime import datetime
# MAIN WINDOW
window = tk.Tk()
window.title("AI Smart Attendance System")
window.state("zoomed")          # Full Screen
window.configure(bg="#F4F6F9")
# MAIN FRAME
main_frame = tk.Frame(window, bg="#F4F6F9")
main_frame.pack(fill="both", expand=True)

canvas = tk.Canvas(
    main_frame,
    bg="#F4F6F9",
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    main_frame,
    orient="vertical",
    command=canvas.yview
)

scroll_frame = tk.Frame(
    canvas,
    bg="#F4F6F9"
)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window(
    (0,0),
    window=scroll_frame,
    anchor="nw"
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)

# Mouse Wheel

def mousewheel(event):
    canvas.yview_scroll(
        int(-1*(event.delta/120)),
        "units"
    )

canvas.bind_all("<MouseWheel>", mousewheel)
# HEADER
header = tk.Frame(
    scroll_frame,
    bg="white",
    relief="ridge",
    bd=2
)

header.pack(
    pady=15,
    anchor="center"
)
# COLLEGE LOGO
try:

    img = Image.open("assets/college_logo.png")

    img = img.resize((120,120))

    logo = ImageTk.PhotoImage(img)

    tk.Label(
        header,
        image=logo,
        bg="white"
    ).pack(pady=(10,5))

except:

    tk.Label(
        header,
        text="COLLEGE LOGO",
        bg="white",
        fg="red",
        font=("Arial",16,"bold")
    ).pack(pady=20)
# TITLES
tk.Label(

    header,

    text="UNITED INSTITUTE OF TECHNOLOGY",

    font=("Arial",26,"bold"),

    fg="#003366",

    bg="white"

).pack()

tk.Label(

    header,

    text="AI SMART ATTENDANCE SYSTEM",

    font=("Arial",18,"bold"),

    fg="green",

    bg="white"

).pack(pady=(5,15))
# DASHBOARD FRAME
dashboard = tk.Frame(
    scroll_frame,
    bg="#F4F6F9"
)

dashboard.pack(
    pady=20,
    anchor="center"
)
# DASHBOARD CARDS
student_card = tk.Label(

    dashboard,

    text="Registered Students\n0",

    bg="#1976D2",

    fg="white",

    width=22,

    height=5,

    font=("Arial",13,"bold")

)

student_card.grid(row=0,column=0,padx=10,pady=10)

present_card = tk.Label(

    dashboard,

    text="Present Today\n0",

    bg="#2E7D32",

    fg="white",

    width=22,

    height=5,

    font=("Arial",13,"bold")

)

present_card.grid(row=0,column=1,padx=10,pady=10)

absent_card = tk.Label(

    dashboard,

    text="Absent Today\n0",

    bg="#D32F2F",

    fg="white",

    width=22,

    height=5,

    font=("Arial",13,"bold")

)

absent_card.grid(row=0,column=2,padx=10,pady=10)
# DATE & TIME
datetime_label = tk.Label(

    scroll_frame,

    text="",

    font=("Arial",12,"bold"),

    bg="#F4F6F9",

    fg="#003366"

)

datetime_label.pack(pady=10)
# DASHBOARD UPDATE
def update_dashboard():

    today = datetime.now().strftime("%d-%m-%Y")

    current_time = datetime.now().strftime("%I:%M:%S %p")

    datetime_label.config(
        text=f"Date : {today}      Time : {current_time}"
    )

    total = 0

    if os.path.exists("images"):

        total = len([

            f

            for f in os.listdir("images")

            if f.lower().endswith(
                (".jpg",".jpeg",".png")
            )

        ])

    attendance_file = os.path.join(

        "Attendance",

        f"Attendance_{today}.csv"

    )

    present = 0

    if os.path.exists(attendance_file):

        with open(attendance_file,"r") as file:

            lines = file.readlines()

            if len(lines) > 1:

                present = len(lines) - 1

    absent = max(0,total-present)

    student_card.config(
        text=f"Registered Students\n{total}"
    )

    present_card.config(
        text=f"Present Today\n{present}"
    )

    absent_card.config(
        text=f"Absent Today\n{absent}"
    )

    window.after(
        1000,
        update_dashboard
    )

update_dashboard()
# COMMON FUNCTION
def run_file(filename):

    try:

        subprocess.Popen([sys.executable, filename])

    except Exception as e:

        messagebox.showerror(
            "Error",
            str(e)
        )
# REGISTER STUDENT
def register_student():

    run_file("register.py")
# GENERATE FACE ENCODINGS
def generate_encodings():

    run_file("encode_faces.py")
# START ATTENDANCE
def start_attendance():

    run_file("attendance.py")
# TODAY'S ATTENDANCE
def view_report():

    today = datetime.now().strftime("%d-%m-%Y")

    file = os.path.join(

        "Attendance",

        f"Attendance_{today}.csv"

    )

    if os.path.exists(file):

        os.startfile(file)

    else:

        messagebox.showwarning(

            "Attendance",

            "Today's Attendance File Not Found."

        )
# SEARCH ATTENDANCE
def search_attendance():

    date = simpledialog.askstring(

        "Search Attendance",

        "Enter Date (DD-MM-YYYY)"

    )

    if not date:
        return

    file = os.path.join(

        "Attendance",

        f"Attendance_{date}.csv"

    )

    if os.path.exists(file):

        os.startfile(file)

    else:

        messagebox.showerror(

            "Error",

            "Attendance File Not Found."

        )
# VIEW STUDENTS
def view_students():

    if not os.path.exists("images"):

        messagebox.showerror(

            "Error",

            "images folder not found."

        )

        return

    students = []

    for file in os.listdir("images"):

        if file.lower().endswith(

            (".jpg",".jpeg",".png")

        ):

            students.append(

                os.path.splitext(file)[0].upper()

            )

    if students:

        messagebox.showinfo(

            "Registered Students",

            "\n".join(students)

        )

    else:

        messagebox.showinfo(

            "Students",

            "No Students Registered."

        )
# DELETE STUDENT
def delete_student():

    name = simpledialog.askstring(

        "Delete Student",

        "Enter Student Name"

    )

    if not name:
        return

    image = os.path.join(

        "images",

        name.upper()+".jpg"

    )

    if os.path.exists(image):

        os.remove(image)

        messagebox.showinfo(

            "Success",

            "Student Deleted Successfully.\nGenerate Encodings Again."

        )

    else:

        messagebox.showerror(

            "Error",

            "Student Not Found."

        )
# UNKNOWN FACES
def open_unknown():

    folder = "Unknown"

    if os.path.exists(folder):

        os.startfile(folder)

    else:

        messagebox.showinfo(

            "Unknown",

            "Unknown Folder Not Found."

        )
# AI FUNCTIONS
def ai_assistant():
    run_file("ai_chat.py")


def ai_parent_email():
    run_file("ai_parent_email.py")


def attendance_analytics():
    run_file("analytics.py")


def generate_pdf():
    run_file("report_generator.py")


def generate_excel():
    run_file("excel_report.py")


def exit_app():

    if messagebox.askyesno(
        "Exit",
        "Do you really want to exit?"
    ):
        window.destroy()
# BUTTONS FRAME
button_frame = tk.Frame(
    scroll_frame,
    bg="#F4F6F9"
)

button_frame.pack(pady=20)

buttons = [

    ("Register Student", register_student, "#28A745"),
    ("Generate Encodings", generate_encodings, "#FF9800"),

    ("Start Attendance", start_attendance, "#E53935"),
    ("Today's Attendance", view_report, "#1976D2"),

    ("Search Attendance", search_attendance, "#6D4C41"),
    ("View Students", view_students, "#00897B"),

    ("Delete Student", delete_student, "#C62828"),
    ("Unknown Faces", open_unknown, "#8E24AA"),

    ("AI Assistant", ai_assistant, "#5E35B1"),
    ("AI Parent Email", ai_parent_email, "#1565C0"),

    ("Attendance Analytics", attendance_analytics, "#00796B"),
    ("Generate PDF", generate_pdf, "#37474F"),

    ("Generate Excel", generate_excel, "#EF6C00"),
    ("Exit", exit_app, "#212121")

]
row = 0
col = 0

for text, command, color in buttons:

    btn = tk.Button(

        button_frame,

        text=text,

        command=command,

        bg=color,

        fg="white",

        font=("Arial",11,"bold"),

        width=22,

        height=2,

        relief="raised",

        bd=2,

        cursor="hand2"

    )

    btn.grid(
        row=row,
        column=col,
        padx=10,
        pady=10
    )

    # Hover Effect
    def enter(e):
        e.widget.config(bg="#00AEEF")

    def leave(e, c=color):
        e.widget.config(bg=c)

    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)

    col += 1

    if col == 2:
        col = 0
        row += 1
# REFRESH BUTTON
refresh_btn = tk.Button(
    scroll_frame,
    text="Refresh Dashboard",
    command=update_dashboard,
    bg="#0D6EFD",
    fg="white",
    font=("Arial",11,"bold"),
    width=25,
    cursor="hand2"
)

refresh_btn.pack(pady=15)
# STATUS BAR
status_var = tk.StringVar()
status_var.set("Ready")

status_bar = tk.Label(
    window,
    textvariable=status_var,
    bg="#003366",
    fg="white",
    anchor="w",
    font=("Arial",10)
)

status_bar.pack(side="bottom", fill="x")
# FOOTER
footer = tk.Label(
    scroll_frame,
    text="United Institute of Technology | AI Smart Attendance System\nDeveloped by Anmol Ojha",
    bg="#F4F6F9",
    fg="gray30",
    font=("Arial",10,"italic"),
    justify="center"
)

footer.pack(pady=20)
# LIVE STATUS BAR
def update_status():

    now = datetime.now().strftime("%d-%m-%Y  %I:%M:%S %p")

    status_var.set(f"Ready | {now}")

    window.after(1000, update_status)

update_status()
# KEYBOARD SHORTCUTS
window.bind("<Escape>", lambda e: exit_app())
window.bind("<F5>", lambda e: update_dashboard())

window.bind("<Control-r>", lambda e: register_student())
window.bind("<Control-a>", lambda e: start_attendance())
window.bind("<Control-e>", lambda e: generate_encodings())
# MOUSE WHEEL FIX
def on_mousewheel(event):

    canvas.yview_scroll(
        int(-1*(event.delta/120)),
        "units"
    )

canvas.bind_all("<MouseWheel>", on_mousewheel)
# WINDOW ICON
try:
    window.iconbitmap("assets/icon.ico")
except:
    pass
# START APPLICATION
window.mainloop()