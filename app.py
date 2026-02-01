from flask import Flask, render_template, request, redirect, url_for,flash
from config import Wa_config,Secret_key
import pymysql

app = Flask(__name__)
app.secret_key = Secret_key


@app.route("/user/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        mobile = request.form.get("mobile")
        password = request.form.get("password")

        conn = pymysql.connect(**Wa_config)
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

        sql = """select * from admin where mobile = %s"""
        data_list = cursor.fetchall()


@app.route("/user/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        mobile = request.form.get("mobile")

        if not all([username, password, mobile]):
            flash("请输入用户名、密码、手机号三个信息", "error")
            return render_template('register.html')

        conn = None
        # 为什么不同cursor = None？ 因为cursor只在try内定义，finally中可能未声明，会导致NameError
        # 为什么不用cursor.close（）？因为conn.close()会自动关闭所有游标，手动关不是必须的
        try:
            conn = pymysql.connect(**Wa_config)
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            sql = """select id from admin where username = %s or mobile = %s"""
            values = [username,mobile]
            cursor.execute(sql,values)
            existing = cursor.fetchone() #返回一个元素是id的元组

            if existing: #非空元组就会进入检查
                sql1 = """select username,mobile from admin where username = %s or mobile = %s"""
                values1 = [username,mobile]
                cursor.execute(sql1,values1)
                user = cursor.fetchone()
                if user["username"] == username:
                    flash("您的用户名已存在","error")
                elif user["mobile"] == mobile:
                    flash("您的手机号码已存在","error")
                return render_template("register.html")
            else:
                sql2 = """insert into admin(username,password,mobile) values(%s,%s,%s)"""
                values2 = [username,password,mobile]
                cursor.execute(sql2,values2)
                conn.commit()
                flash("注册成功","success")
                return redirect(url_for('login'))  # 'login' 是 login 函数的名称
        except Exception as e:
            print(f"注册失败：{e}")
            flash("注册失败","error")
            return render_template("register.html")
        finally:
            if conn:
                conn.close()





@app.route("/user/account", methods=["GET", "POST"])
def account():
    return render_template("account.html")


if __name__ == "__main__":
    app.run()
