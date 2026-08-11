from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("database.db")
    return conn

def init_db():
    conn = connect_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            roll TEXT,
            m1 INTEGER,
            m2 INTEGER,
            m3 INTEGER,
            total INTEGER,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        m1 = int(request.form["m1"])
        m2 = int(request.form["m2"])
        m3 = int(request.form["m3"])
        total = m1 + m2 + m3
        avg = total / 3
        if avg >= 35:
            result = "Pass"
        else:
            result = "Fail"
        conn = connect_db()
        conn.execute(
            "INSERT INTO results(name,roll,m1,m2,m3,total,result) VALUES(?,?,?,?,?,?,?)",
            (name, roll, m1, m2, m3, total, result)
        )
        conn.commit()
        conn.close()
        return redirect("/results")
    return render_template("add_result.html")

@app.route("/results")
def results():
    conn = connect_db()
    data = conn.execute("SELECT * FROM results").fetchall()
    conn.close()
    return render_template("results.html", students=data)

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
