import os
import csv
import pickle
import numpy as np
import pandas as pd
from PIL import Image
from datetime import datetime
import face_recognition

def load_encodings():
    if not os.path.exists("encodings.pkl"):
        return {"encodings": [], "names": []}
    try:
        with open("encodings.pkl", "rb") as f:
            return pickle.load(f)
    except Exception:
        return {"encodings": [], "names": []}

def save_encodings(encodings, names):
    with open("encodings.pkl", "wb") as f:
        pickle.dump({"encodings": encodings, "names": names}, f)

def get_registered_students():
    students = set()
    if os.path.exists("images"):
        for f in os.listdir("images"):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                students.add(os.path.splitext(f)[0].upper())
    data = load_encodings()
    for name in data.get("names", []):
        students.add(name.upper())
    return sorted(list(students))

def get_today_file():
    os.makedirs("Attendance", exist_ok=True)
    today = datetime.now().strftime("%d-%m-%Y")
    return os.path.join("Attendance", f"Attendance_{today}.csv")

def get_today_attendance():
    path = get_today_file()
    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            return df
        except Exception:
            pass
    return pd.DataFrame(columns=["Name", "Time", "Status"])

def mark_student_attendance(student_name):
    path = get_today_file()
    now_time = datetime.now().strftime("%H:%M:%S")
    student_name = student_name.strip().upper()

    if os.path.exists(path):
        try:
            df = pd.read_csv(path)
            if not df.empty and "Name" in df.columns:
                present_names = [str(x).upper() for x in df["Name"].tolist()]
                if student_name in present_names:
                    return False, f"Attendance already marked today for {student_name}."
        except Exception:
            pass
    else:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Time", "Status"])

    with open(path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([student_name, now_time, "Present"])

    return True, f"Attendance marked for {student_name} at {now_time}!"

def match_faces_in_image(pil_image):
    rgb_img = np.array(pil_image.convert("RGB"))
    face_locations = face_recognition.face_locations(rgb_img)
    if not face_locations:
        return [], "No face detected in the picture. Please ensure proper lighting and face the camera directly."

    encodings_data = load_encodings()
    known_encodings = encodings_data.get("encodings", [])
    known_names = [n.upper() for n in encodings_data.get("names", [])]

    if not known_encodings:
        return [], "Face database is empty. Please register students first under 'Register Student'."

    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
    results = []

    for face_encoding in face_encodings:
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_idx = np.argmin(face_distances)
        best_dist = face_distances[best_idx]

        if best_dist < 0.50:
            name = known_names[best_idx]
            confidence = round(float((1 - best_dist) * 100), 1)
            results.append({"name": name, "confidence": confidence, "status": "Matched"})
        else:
            confidence = round(float((1 - best_dist) * 100), 1)
            results.append({"name": "UNKNOWN", "confidence": confidence, "status": "Unknown"})

    return results, None

def register_new_student(name, pil_image):
    name_clean = name.strip().upper()
    if not name_clean:
        return False, "Please provide a student name."

    rgb_img = np.array(pil_image.convert("RGB"))
    encodings = face_recognition.face_encodings(rgb_img)
    if not encodings:
        return False, "No face detected in the photo. Please capture a clear face photo."

    os.makedirs("images", exist_ok=True)
    save_path = os.path.join("images", f"{name_clean}.jpg")
    pil_image.convert("RGB").save(save_path)

    data = load_encodings()
    encodings_list = list(data.get("encodings", []))
    names_list = list(data.get("names", []))

    if name_clean in [n.upper() for n in names_list]:
        idx = [n.upper() for n in names_list].index(name_clean)
        encodings_list[idx] = encodings[0]
        names_list[idx] = name_clean
    else:
        encodings_list.append(encodings[0])
        names_list.append(name_clean)

    save_encodings(encodings_list, names_list)
    return True, f"Student '{name_clean}' registered successfully!"
