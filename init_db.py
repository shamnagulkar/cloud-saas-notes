import sqlite3

conn = sqlite3.connect("notes.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")
