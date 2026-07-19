import os
import cv2
import tkinter as tk
from tkinter import simpledialog, messagebox

path = "images"
os.makedirs(path, exist_ok=True)

# Hidden Tkinter window
root = tk.Tk()
root.withdraw()

name = simpledialog.askstring("Student Registration", "Enter Student Name:")

if not name:
    messagebox.showerror("Error", "Student Name Required")
    exit()

name = name.strip().upper()

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    messagebox.showerror("Error", "Camera Not Found")
    exit()

messagebox.showinfo(
    "Instructions",
    "Press 'S' to Save Photo\nPress 'Q' to Exit"
)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("Student Registration", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):

        filename = os.path.join(path, f"{name}.jpg")
        cv2.imwrite(filename, frame)

        messagebox.showinfo("Success", f"{name} Registered Successfully")

        break

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()