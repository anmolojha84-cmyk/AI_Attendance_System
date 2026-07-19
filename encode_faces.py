import cv2
import face_recognition
import os
import pickle

path = "images"

images = []
classNames = []

print("Loading Images...")

for file in os.listdir(path):

    img = cv2.imread(os.path.join(path, file))

    if img is None:
        continue

    images.append(img)
    classNames.append(os.path.splitext(file)[0])

print("Creating Face Encodings...")

encodeList = []

for img in images:

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    encodes = face_recognition.face_encodings(rgb)

    if len(encodes) > 0:
        encodeList.append(encodes[0])

data = {
    "encodings": encodeList,
    "names": classNames
}

with open("encodings.pkl", "wb") as f:
    pickle.dump(data, f)

print("Encodings Saved Successfully")