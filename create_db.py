import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users(username,password)
VALUES(?,?)
""",("admin","admin123"))

conn.commit()
conn.close()

print("Database Created Successfully")