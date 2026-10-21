import pyttsx3

engine = pyttsx3.init()

engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

engine.say("Attendance marked successfully")
engine.runAndWait()