from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect_db():
    conn = sqlite3.connect("database.db")
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET","POST"])
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
        (name,roll,m1,m2,m3,total,result)
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


app.run(debug=True)