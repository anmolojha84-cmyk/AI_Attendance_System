import tkinter as tk
from tkinter import messagebox
import smtplib

from email.mime.text import MIMEText

from google import genai

from config import GEMINI_API_KEY
from email_config import EMAIL, APP_PASSWORD

# ----------------------------
# Gemini Client
# ----------------------------

client = genai.Client(
    api_key=GEMINI_API_KEY
)
# ======================================
# Generate Parent Email
# ======================================

def generate_email():

    student = name_entry.get().strip()
    attendance = attendance_entry.get().strip()

    if student == "" or attendance == "":
        messagebox.showerror(
            "Error",
            "Enter Student Name and Attendance"
        )
        return

    # Accept both 58 and 58%
    attendance = attendance.replace("%", "").strip()

    try:
        attendance = int(attendance)

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Attendance must be like 58 or 58%"
        )
        return

    prompt = f"""
You are an AI Attendance Assistant.

Write a professional email to the parent.

Student Name : {student}

Attendance : {attendance}%

The email must include:

1. Greeting
2. Attendance Status
3. Performance
4. Suggestions
5. Motivation
6. Thank You

Keep it under 150 words.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        email = response.text

    except Exception as e:

        print("Gemini Error :", e)

        # Local AI Fallback
        if attendance >= 90:

            email = f"""
Subject: Excellent Attendance

Dear Parent,

We are pleased to inform you that your child {student} has maintained an outstanding attendance of {attendance}%.

The attendance record reflects excellent discipline and commitment.

Please continue motivating your child.

Thank you.

Regards,
United Institute of Technology
"""

        elif attendance >= 75:

            email = f"""
Subject: Good Attendance

Dear Parent,

Your child {student} has maintained {attendance}% attendance.

Attendance is satisfactory.

We encourage maintaining this consistency.

Thank you.

Regards,
United Institute of Technology
"""

        else:

            email = f"""
Subject: Low Attendance Alert

Dear Parent,

This is to inform you that your child {student} has only {attendance}% attendance.

Low attendance may affect academic performance and university eligibility.

Kindly encourage your child to attend classes regularly.

Thank you.

Regards,
United Institute of Technology
"""

    output.delete("1.0", tk.END)
    output.insert(tk.END, email)
    # ======================================
# Copy Email
# ======================================

def copy_email():

    text = output.get("1.0", tk.END)

    root.clipboard_clear()
    root.clipboard_append(text)

    messagebox.showinfo(
        "Success",
        "Email Copied Successfully"
    )


# ======================================
# Send Email
# ======================================

def send_email():

    parent_email = parent_entry.get().strip()

    if parent_email == "":
        messagebox.showerror(
            "Error",
            "Enter Parent Email"
        )
        return

    if "@" not in parent_email or "." not in parent_email:

        messagebox.showerror(
            "Error",
            "Invalid Email Address"
        )
        return

    body = output.get("1.0", tk.END)

    if body.strip() == "":

        messagebox.showerror(
            "Error",
            "Generate Email First"
        )
        return

    msg = MIMEText(body)

    msg["Subject"] = "Student Attendance Report"

    msg["From"] = EMAIL

    msg["To"] = parent_email

    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            EMAIL,
            APP_PASSWORD
        )

        server.send_message(msg)

        server.quit()

        messagebox.showinfo(
            "Success",
            "Email Sent Successfully"
        )

    except Exception as e:

        messagebox.showerror(
            "Email Error",
            str(e)
        )
        # ======================================
# GUI
# ======================================

root = tk.Tk()

root.title("AI Parent Email Generator")

root.geometry("800x700")

root.configure(bg="white")

# ----------------------------
# Title
# ----------------------------

tk.Label(
    root,
    text="UNITED INSTITUTE OF TECHNOLOGY",
    font=("Arial",18,"bold"),
    fg="navy",
    bg="white"
).pack(pady=5)

tk.Label(
    root,
    text="AI PARENT EMAIL GENERATOR",
    font=("Arial",15,"bold"),
    fg="green",
    bg="white"
).pack(pady=10)

# ----------------------------
# Student Name
# ----------------------------

tk.Label(
    root,
    text="Student Name",
    font=("Arial",11),
    bg="white"
).pack()

name_entry = tk.Entry(
    root,
    width=40,
    font=("Arial",11)
)

name_entry.pack(pady=5)

# ----------------------------
# Attendance
# ----------------------------

tk.Label(
    root,
    text="Attendance (%)",
    font=("Arial",11),
    bg="white"
).pack()

attendance_entry = tk.Entry(
    root,
    width=40,
    font=("Arial",11)
)

attendance_entry.pack(pady=5)

# ----------------------------
# Parent Email
# ----------------------------

tk.Label(
    root,
    text="Parent Email",
    font=("Arial",11),
    bg="white"
).pack()

parent_entry = tk.Entry(
    root,
    width=40,
    font=("Arial",11)
)

parent_entry.pack(pady=5)

# ----------------------------
# Buttons
# ----------------------------

tk.Button(
    root,
    text="Generate AI Email",
    bg="green",
    fg="white",
    font=("Arial",11,"bold"),
    width=25,
    command=generate_email
).pack(pady=8)

tk.Button(
    root,
    text="Copy Email",
    bg="blue",
    fg="white",
    font=("Arial",11,"bold"),
    width=25,
    command=copy_email
).pack(pady=5)

tk.Button(
    root,
    text="Send Email",
    bg="purple",
    fg="white",
    font=("Arial",11,"bold"),
    width=25,
    command=send_email
).pack(pady=5)

# ----------------------------
# Output Box
# ----------------------------

output = tk.Text(
    root,
    width=90,
    height=18,
    font=("Arial",10)
)

output.pack(pady=15)

# ----------------------------
# Footer
# ----------------------------

tk.Label(
    root,
    text="Developed By : Anmol Ojha",
    font=("Arial",10,"italic"),
    fg="gray",
    bg="white"
).pack(pady=10)

root.mainloop()