import tkinter as tk
from tkinter import scrolledtext
import pandas as pd
import os
from datetime import datetime

# ===============================
# Read Today's Attendance
# ===============================

today = datetime.now().strftime("%d-%m-%Y")

attendance_file = os.path.join(
    "Attendance",
    f"Attendance_{today}.csv"
)

attendance_data = ""

if os.path.exists(attendance_file):
    df = pd.read_csv(attendance_file)
    attendance_data = df.to_string(index=False)
else:
    attendance_data = "No attendance available for today."

# ===============================
# Offline AI Assistant
# ===============================

try:
    import ai_assistant
except Exception:
    ai_assistant = None

def ask_ai():
    question = entry.get().strip()

    if question == "":
        output.delete("1.0", tk.END)
        output.insert(tk.END, "Please enter your question.")
        return

    output.delete("1.0", tk.END)
    output.insert(tk.END, "Thinking...")
    window.update()

    if ai_assistant:
        try:
            answer = ai_assistant.answer_attendance_query(question)
        except Exception as e:
            answer = f"Error: {e}"
    else:
        answer = f"Today's Attendance:\n{attendance_data}"

    output.delete("1.0", tk.END)
    output.insert(tk.END, answer)
    # ======================================
# GUI
# ======================================

window = tk.Tk()
window.title("AI Attendance Assistant")
window.geometry("850x650")
window.configure(bg="#F4F6F9")

# -----------------------------
# Header
# -----------------------------

tk.Label(
    window,
    text="UNITED INSTITUTE OF TECHNOLOGY",
    font=("Arial",18,"bold"),
    fg="#003366",
    bg="#F4F6F9"
).pack(pady=(15,5))

tk.Label(
    window,
    text="AI ATTENDANCE ASSISTANT (OFFLINE)",
    font=("Arial",15,"bold"),
    fg="green",
    bg="#F4F6F9"
).pack(pady=(0,20))

# -----------------------------
# Question Label
# -----------------------------

tk.Label(
    window,
    text="Ask Your Question",
    font=("Arial",11,"bold"),
    bg="#F4F6F9"
).pack()

# -----------------------------
# Entry Box
# -----------------------------

entry = tk.Entry(
    window,
    width=70,
    font=("Arial",12)
)

entry.pack(pady=8)

# -----------------------------
# Button Frame
# -----------------------------

button_frame = tk.Frame(
    window,
    bg="#F4F6F9"
)

button_frame.pack(pady=10)

# Ask Button

tk.Button(
    button_frame,
    text="Ask AI",
    command=ask_ai,
    bg="green",
    fg="white",
    width=15,
    font=("Arial",11,"bold")
).grid(row=0,column=0,padx=10)

# Clear Button

def clear_chat():

    entry.delete(0,tk.END)
    output.delete("1.0",tk.END)

tk.Button(
    button_frame,
    text="Clear",
    command=clear_chat,
    bg="orange",
    fg="white",
    width=15,
    font=("Arial",11,"bold")
).grid(row=0,column=1,padx=10)

# Exit Button

tk.Button(
    button_frame,
    text="Exit",
    command=window.destroy,
    bg="red",
    fg="white",
    width=15,
    font=("Arial",11,"bold")
).grid(row=0,column=2,padx=10)

# -----------------------------
# Output Label
# -----------------------------

tk.Label(
    window,
    text="AI Response",
    font=("Arial",11,"bold"),
    bg="#F4F6F9"
).pack(pady=(10,5))

# -----------------------------
# Output Box
# -----------------------------

output = scrolledtext.ScrolledText(
    window,
    width=95,
    height=22,
    font=("Consolas",10)
)

output.pack(pady=10)

output.insert(
    tk.END,
    """Welcome to AI Attendance Assistant

You can ask questions like:

• Today's attendance
• Attendance
• Present students
• Registered students
• Total students
• About project
• Developer
• Help

"""
)

# -----------------------------
# Footer
# -----------------------------

tk.Label(
    window,
    text="Developed By : Anmol Ojha | AI Smart Attendance Monitoring System",
    font=("Arial",10,"italic"),
    fg="gray30",
    bg="#F4F6F9"
).pack(pady=15)

# -----------------------------
# Enter Key Support
# -----------------------------

entry.bind("<Return>", lambda event: ask_ai())

# -----------------------------
# Run Window
# -----------------------------

window.mainloop()