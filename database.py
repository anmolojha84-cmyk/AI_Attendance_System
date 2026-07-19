import sqlite3

import os
import sqlite3

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect("database/attendance.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    photo TEXT
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")