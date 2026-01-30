from flask import Flask,render_template,request
from config import Wa_config
import pymysql

conn = pymysql.connect(**Wa_config) #字典解包
cursor = conn.cursor(cursor = pymysql.cursor.DictCursor)

app = Flask(__name__)

@app.route("/user/login",methods = ["GET","POST"])
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run()