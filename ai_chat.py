import tkinter as tk
from tkinter import scrolledtext
from google import genai
from config import GEMINI_API_KEY
import pandas as pd
import os
from datetime import datetime

# Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Read Today's Attendance
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
    attendance_data = "No attendance available."

# Ask AI
def ask_ai():

    question = entry.get()

    prompt = f"""
You are an AI Attendance Assistant.

Today's Attendance:

{attendance_data}

Teacher Question:

{question}

Answer briefly and professionally.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        output.delete("1.0", tk.END)
        output.insert(tk.END, response.text)

    except Exception as e:

        output.delete("1.0", tk.END)
        output.insert(tk.END, str(e))


# GUI
window = tk.Tk()
window.title("AI Attendance Assistant")
window.geometry("600x500")

tk.Label(
    window,
    text="Ask AI About Attendance",
    font=("Arial",16,"bold")
).pack(pady=10)

entry = tk.Entry(
    window,
    width=60
)

entry.pack(pady=5)

tk.Button(
    window,
    text="Ask AI",
    command=ask_ai,
    bg="green",
    fg="white"
).pack(pady=10)

output = scrolledtext.ScrolledText(
    window,
    width=70,
    height=18
)

output.pack(pady=10)

window.mainloop()