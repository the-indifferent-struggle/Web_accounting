from flask import Flask,render_template,request
from config import Wa_config
import pymysql



app = Flask(__name__)

@app.route("/user/login",methods = ["GET","POST"])
def login():
    return render_template("login.html")

@app.route("/user/register",methods = ["GET","POST"])
def register():
    return render_template("register.html")

if __name__ == "__main__":
    app.run()