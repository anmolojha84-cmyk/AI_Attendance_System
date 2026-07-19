import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ======================================
# Total Students in Class
# ======================================

TOTAL_STUDENTS = 10

# ======================================
# Today's Attendance File
# ======================================

today = datetime.now().strftime("%d-%m-%Y")

attendance_file = os.path.join(
    "Attendance",
    f"Attendance_{today}.csv"
)

# ======================================
# Check Attendance File
# ======================================

if not os.path.exists(attendance_file):

    print("=" * 50)
    print("Attendance File Not Found!")
    print("=" * 50)
    exit()

# ======================================
# Read CSV File
# ======================================

df = pd.read_csv(attendance_file)

if df.empty:

    print("Attendance File is Empty!")
    exit()

# ======================================
# Attendance Data
# ======================================

students = df["Name"].tolist()

present = len(students)

absent = max(0, TOTAL_STUDENTS - present)

attendance_percentage = round(
    (present / TOTAL_STUDENTS) * 100,
    2
)

# ======================================
# Console Summary
# ======================================

print("=" * 45)
print("AI SMART ATTENDANCE ANALYTICS")
print("=" * 45)

print("Date :", today)
print("Total Students :", TOTAL_STUDENTS)
print("Present :", present)
print("Absent :", absent)
print("Attendance Percentage :", attendance_percentage, "%")

print("=" * 45)

# ======================================
# Bar Chart
# ======================================

plt.figure(figsize=(9, 5))

plt.bar(
    students,
    [1] * present
)

plt.title("Today's Attendance")

plt.xlabel("Students")

plt.ylabel("Attendance")

plt.yticks([0, 1], ["Absent", "Present"])

plt.grid(axis="y")

plt.tight_layout()

plt.show()

# ======================================
# Pie Chart
# ======================================

plt.figure(figsize=(6, 6))

plt.pie(
    [present, absent],
    labels=["Present", "Absent"],
    autopct="%1.1f%%",
    startangle=90
)

plt.title("Attendance Percentage")

plt.tight_layout()

plt.show()

# ======================================
# Student List
# ======================================

print("\nPresent Students:\n")

for i, student in enumerate(students, start=1):

    print(f"{i}. {student}")

print("\nAnalytics Completed Successfully.")