from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)
DB_NAME = "testdb.sqlite"

# ✅ Function to get a DB connection
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row   # makes rows behave like dictionaries
    return conn

# ✅ Create the users table if it doesn't exist
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    conn.close()
    return render_template("webtest.html", users=users)

@app.route("/add", methods=["POST"])
def add_data():
    name = request.form["name"]
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/update/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        new_name = request.form["name"]
        cur.execute("UPDATE users SET name = ? WHERE id = ?", (new_name, user_id))
        conn.commit()
        conn.close()
        return redirect(url_for("home"))
    else:
        cur.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        conn.close()
        return render_template("update.html", user=user)

if __name__ == "__main__":
    init_db()  # make sure table exists
    app.run(debug=True)
