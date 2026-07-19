import cv2
import face_recognition
import numpy as np
import pickle
import csv
import os
import time
import threading
import pythoncom
import win32com.client
from datetime import datetime
# AI SMART ATTENDANCE SYSTEM
print("=" * 60)
print("         AI SMART ATTENDANCE SYSTEM")
print("=" * 60)
# WINDOWS VOICE ASSISTANT
voice_lock = threading.Lock()

def speak(text):

    def run():

        with voice_lock:

            try:

                pythoncom.CoInitialize()

                speaker = win32com.client.Dispatch("SAPI.SpVoice")

                speaker.Volume = 100
                speaker.Rate = 0

                speaker.Speak(text)

                pythoncom.CoUninitialize()

            except Exception as e:

                print("Voice Error :", e)

    threading.Thread(target=run, daemon=True).start()
# GLOBAL VARIABLES
spoken_students = set()

last_unknown_voice = 0
last_unknown_save = 0
scanner_y = 0
# LOAD FACE DATABASE
print("Loading Face Database...")

if not os.path.exists("encodings.pkl"):

    print("encodings.pkl not found")
    speak("Face database not found.")
    exit()

with open("encodings.pkl", "rb") as file:
    data = pickle.load(file)
knownEncodings = data["encodings"]
knownNames = [x.upper() for x in data["names"]]
print("Students Loaded :", knownNames)
# ATTENDANCE FOLDER
os.makedirs("Attendance", exist_ok=True)
os.makedirs("Unknown", exist_ok=True)
today = datetime.now().strftime("%d-%m-%Y")
attendance_file = os.path.join(
    "Attendance",
    f"Attendance_{today}.csv"
)
# Create CSV
if not os.path.exists(attendance_file):

    with open(attendance_file, "w", newline="") as file:

        writer = csv.writer(file)
        writer.writerow(["Name", "Time"])

print("Attendance File Ready")
# CAMERA
print("Opening Camera...")

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():

    print("Camera Not Found")
    speak("Camera not found.")
    exit()

print("Camera Started Successfully")

speak("AI Smart Attendance System is ready.")
# MARK ATTENDANCE
def markAttendance(name):

    # Read Today's Attendance
    with open(attendance_file, "r", newline="") as file:

        reader = csv.reader(file)
        next(reader, None)

        present = {
            row[0].strip().upper()
            for row in reader
            if row
        }

    # Already Present
    if name.upper() in present:
        return False

    # Current Time
    current_time = datetime.now().strftime("%I:%M:%S %p")

    # Save Attendance
    with open(attendance_file, "a", newline="") as file:

        writer = csv.writer(file)
        writer.writerow([name, current_time])

    print("=" * 60)
    print("ATTENDANCE MARKED SUCCESSFULLY")
    print("Student :", name)
    print("Time    :", current_time)
    print("=" * 60)

    # Voice
    speak(f"{name}, your attendance has been marked successfully. Welcome.")

    return True

# SAVE UNKNOWN FACE
def saveUnknown(face):

    global last_unknown_save

    if face.size == 0:
        return

    current = time.time()

    # Save Every 5 Seconds
    if current - last_unknown_save < 5:
        return

    filename = os.path.join(
        "Unknown",
        "Unknown_" +
        datetime.now().strftime("%d-%m-%Y_%H-%M-%S") +
        ".jpg"
    )

    cv2.imwrite(filename, face)

    print("Unknown Face Saved :", filename)

    last_unknown_save = current
# SYSTEM READY
print("System Ready...")
speak("System is ready. Camera started successfully.")
# FACE RECOGNITION LOOP
while True:

    success, img = cap.read()

    if not success:
        print("Camera Error")
        break

    # Mirror View
    img = cv2.flip(img, 1)

    # Small Image For Fast Recognition
    small = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    # Detect Faces
    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(
        rgb,
        face_locations
    )

    # Every Face
    for encodeFace, faceLoc in zip(face_encodings, face_locations):

        matches = face_recognition.compare_faces(
            knownEncodings,
            encodeFace,
            tolerance=0.45
        )

        face_distance = face_recognition.face_distance(
            knownEncodings,
            encodeFace
        )

        if len(face_distance) == 0:
            continue

        matchIndex = np.argmin(face_distance)

        y1, x2, y2, x1 = faceLoc

        y1 *= 4
        x2 *= 4
        y2 *= 4
        x1 *= 4
        # KNOWN PERSON
        if matches[matchIndex] and face_distance[matchIndex] < 0.45:

            name = knownNames[matchIndex]

            confidence = int(
                (1 - face_distance[matchIndex]) * 100
            )
            confidence = max(0, min(confidence, 100))
            # Green Box
            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (0,255,0),
                2
            )

            cv2.rectangle(
                img,
                (x1, y2-35),
                (x2, y2),
                (0,255,0),
                cv2.FILLED
            )

            cv2.putText(
                img,
                f"{name} ({confidence}%)",
                (x1+5, y2-8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255,255,255),
                2
            )

            # Attendance Only Once
            if name not in spoken_students:

                if markAttendance(name):

                    spoken_students.add(name)
        # UNKNOWN PERSON
        else:

            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (0,0,255),
                2
            )

            cv2.rectangle(
                img,
                (x1, y2-35),
                (x2, y2),
                (0,0,255),
                cv2.FILLED
            )

            cv2.putText(
                img,
                "UNKNOWN",
                (x1+5, y2-8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255,255,255),
                2
            )

            current = time.time()

            # Unknown Voice Every 5 Seconds
            if current - last_unknown_voice > 5:

                speak("Warning. Unknown person detected.")

                last_unknown_voice = current

            # Save Unknown Face
            saveUnknown(
                img[y1:y2, x1:x2]
            )
            
# DASHBOARD
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    if fps <= 0:
        fps = 30

    # Header
    cv2.rectangle(img, (0, 0), (img.shape[1], 45), (45, 45, 45), -1)

    cv2.putText(
        img,
        "AI SMART ATTENDANCE SYSTEM",
        (310, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,255),
        2
    )

    # Date
    cv2.putText(
        img,
        datetime.now().strftime("Date : %d-%m-%Y"),
        (10,70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,255,255),
        2
    )

    # Time
    cv2.putText(
        img,
        datetime.now().strftime("Time : %I:%M:%S %p"),
        (10,100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,255,255),
        2
    )

    # FPS
    cv2.putText(
        img,
        f"FPS : {fps}",
        (10,130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0,255,255),
        2
    )

    # Camera Status
    cv2.putText(
        img,
        "Camera : ON",
        (10,160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0,255,0),
        2
    )

    # Registered Students
    cv2.putText(
        img,
        f"Registered : {len(knownNames)}",
        (10,190),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255,255,255),
        2
    )

    # Today's Present
    cv2.putText(
        img,
        f"Present : {len(spoken_students)}",
        (10,220),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0,255,0),
        2
    )

    # Scanner Animation
    scanner_y += 5

    if scanner_y >= img.shape[0]:
        scanner_y = 0

    cv2.line(
        img,
        (0, scanner_y),
        (img.shape[1], scanner_y),
        (255,255,0),
        2
    )

    # Border
    cv2.rectangle(
        img,
        (5,5),
        (img.shape[1]-5, img.shape[0]-5),
        (0,255,0),
        2
    )

    # Footer
    cv2.rectangle(
        img,
        (0,img.shape[0]-35),
        (img.shape[1],img.shape[0]),
        (40,40,40),
        -1
    )

    cv2.putText(
        img,
        "Developed By : Anmol Ojha",
        (15,img.shape[0]-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255,255,255),
        1
    )

    cv2.putText(
        img,
        "Press Q To Exit",
        (img.shape[1]-170,img.shape[0]-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0,255,255),
        1
    )
    # Show Window
    cv2.imshow("AI Smart Attendance System", img)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        speak("Thank you for using AI Smart Attendance System.")
        break
# CLEANUP
cap.release()
cv2.destroyAllWindows()
print("=" * 60)
print("AI SMART ATTENDANCE SYSTEM CLOSED")
print("=" * 60)