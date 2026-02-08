from flask import Flask, render_template, request, redirect, url_for, flash,session
from config import Wa_config, Secret_key
from datetime import date
import pymysql
import models

app = Flask(__name__)
app.secret_key = Secret_key


@app.route("/user/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        mobile = request.form.get("mobile")
        password = request.form.get("password")

        if not all([mobile, password]):
            flash("请输入完整的用户名和密码", "error")
            return render_template("login.html")

        try:
            conn = pymysql.connect(**Wa_config)
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            sql = """select id
                     from admin
                     where mobile = %s"""
            values = [mobile, ]
            cursor.execute(sql, values)
            existing = cursor.fetchone()

            if existing:
                sql = """select password
                         from admin
                         where mobile = %s"""
                values = [mobile, ]
                cursor.execute(sql, values)
                data_dict = cursor.fetchone()
                if data_dict["password"] == password:
                    flash("登录成功", "success")
                    return redirect(url_for("account"))
                else:
                    flash("密码错误", "error")
                    return render_template("login.html")
            else:
                print("该手机号码不存在")
                flash("手机号码不存在", "error")
                return render_template("login.html")
        except Exception as e:
            print(f"登录失败：{e}")
            flash("登录失败", "error")
            return render_template("login.html")
        finally:
            if conn:
                conn.close()


@app.route("/user/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        mobile = request.form.get("mobile")

        if not all([username, password, mobile]):
            flash("请输入完整的用户名、密码、手机号", "error")
            return render_template('register.html')

        conn = None
        # 为什么不同cursor = None？ 因为cursor只在try内定义，finally中可能未声明，会导致NameError
        # 为什么不用cursor.close（）？因为conn.close()会自动关闭所有游标，手动关不是必须的
        try:
            conn = pymysql.connect(**Wa_config)
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

            sql = """select id
                     from admin
                     where username = %s
                        or mobile = %s"""
            values = [username, mobile]
            cursor.execute(sql, values)
            existing = cursor.fetchone()  # 返回一个元素是id的元组

            if existing:  # 非空元组就会进入检查
                sql1 = """select username, mobile
                          from admin
                          where username = %s
                             or mobile = %s"""
                values1 = [username, mobile]
                cursor.execute(sql1, values1)
                user = cursor.fetchone()
                if user["username"] == username:
                    flash("您的用户名已存在", "error")
                elif user["mobile"] == mobile:
                    flash("您的手机号码已存在", "error")
                return render_template("register.html")
            else:
                sql2 = """insert into admin(username, password, mobile)
                          values (%s, %s, %s)"""
                values2 = [username, password, mobile]
                cursor.execute(sql2, values2)
                conn.commit()
                flash("注册成功", "success")
                return redirect(url_for('login'))  # 'login' 是 login 函数的名称
        except Exception as e:
            print(f"注册失败：{e}")
            flash("注册失败", "error")
            return render_template("register.html")
        finally:
            if conn:
                conn.close()


@app.route("/user/account", methods=["GET", "POST"])
def account():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    today_str = date.today().isoformat()

    if request.method == "GET":
        search_date = request.args.get("date")

        if search_date:
            records = models.get_records_by_date(user_id,search_date)
        else:
            records = models.get_all_records(user_id)

        for r in records:
            if r["type"] == "income":
                r["type"] = "收入"
            else:
                r["type"] = "支出"

        return render_template("account.html",data_list = records,today = today_str,date = search_date)
    else:
        action = request.form.get("action")
        if action == "add":
            amount = request.form.get("amount")
            type_chinese = request.form.get("type")
            category = request.form.get("category")
            date_val = request.form.get("date")
            description = request.form.get("description")

            if not all([amount,type_chinese,category,date_val]):
                flash("请填写完整信息","error")
                return redirect(url_for("account"))

            try:
                models.add_record(user_id, amount, type_chinese, category, date_val, description)
                flash("增加成功","success")
            except Exception as e:
                print(f"新增失败:{e}")
                flash("增加失败","error")
            return redirect(url_for("account"))

        elif action=="update":
            record_id = request.form.get("record_id")
            amount =  request.form.get("amount")
            type_chinese = request.form.get("type")
            category = request.form.get("category")
            date_val = request.form.get("date")
            description = request.form.get("description")

            if not all([record_id, amount, type_chinese, category, date_val]):
                flash("请填写完整信息", "error")
                return redirect(url_for('account'))

            try:
                success = models.update_record(record_id, user_id, amount, type_chinese, category, date_val,description)
                if success:
                    flash("修改成功！", "success")
                else:
                    flash("无法修改此记录", "error")
            except Exception as e:
                print(f"修改失败: {e}")
                flash("修改失败", "error")
            return redirect(url_for('account'))

        elif action == 'delete':
            record_id = request.form.get('record_id')
            if not record_id:
                flash("查无此纪录", "error")
                return redirect(url_for('account'))

            try:
                success = models.delete_record(record_id, user_id)
                if success:
                    flash("删除成功！", "success")
                else:
                    flash("无法删除此记录", "error")
            except Exception as e:
                print(f"删除失败: {e}")
                flash("删除失败", "error")
            return redirect(url_for('account'))

        else:
            flash("未知操作","error")
            return redirect(url_for('account'))


if __name__ == "__main__":
    app.run()
