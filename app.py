from flask import Flask, render_template, request
from config import Wa_config
import pymysql

app = Flask(__name__)


@app.route("/user/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")


@app.route("/user/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        mobile = request.form.get("mobile")

        conn = pymysql.connect(**Wa_config)
        cursor = conn.cursor(cursors = pymysql.cursor.Dict)


@app.route("/user/account", methods=["GET", "POST"])
def account():
    return render_template("account.html")


if __name__ == "__main__":
    app.run()
