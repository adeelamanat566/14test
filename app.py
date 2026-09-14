from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)


def get_db():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "db"),
        user=os.getenv("MYSQL_USER", "myuser"),
        password=os.getenv("MYSQL_PASSWORD", "mypassword"),
        database=os.getenv("MYSQL_DATABASE", "mydb")
    )


@app.route("/")
def home():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT id, name FROM users")
    users = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("index.html", users=users)


@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO users (name) VALUES (%s)",
        (name,)
    )

    db.commit()

    cursor.close()
    db.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)