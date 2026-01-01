from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

# -------------------------------
# Memoir - Personal Notes SaaS
# -------------------------------

app = Flask(__name__)
DB_NAME = "notes.db"


# ---------- Database Helper ----------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Initialize Database ----------
def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# ---------- Routes ----------
@app.route("/", methods=["GET", "POST"])
def home():
    conn = get_db_connection()

    if request.method == "POST":
        note = request.form.get("note")
        if note:
            conn.execute(
                "INSERT INTO notes (content, created_at) VALUES (?, ?)",
                (note, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )
            conn.commit()

    notes = conn.execute(
        "SELECT * FROM notes ORDER BY id DESC"
    ).fetchall()

    conn.close()
    return render_template("index.html", notes=notes)


@app.route("/delete/<int:note_id>")
def delete_note(note_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))


# ---------- Main ----------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
