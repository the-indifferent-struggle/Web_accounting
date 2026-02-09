import pymysql
from config import Wa_config

def add_record(user_id,amount,type_chinese,category,date_val,description):
    type_map = {"收入":"income","支出":"expense"}
    type_english = type_map.get(type_chinese,"expense")
    conn = pymysql.connect(**Wa_config)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    try:
        sql = """insert into account(user_id,amount,type,category,date,description) values(%s,%s,%s,%s,%s,%s)"""
        values = [user_id,amount,type_english,category,date_val,description]

        cursor.execute(sql,values)
        conn.commit()
    finally:
        conn.close()

def delete_record(record_id, user_id):
    conn = pymysql.connect(**Wa_config)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        sql = """DELETE FROM account WHERE id = %s AND user_id = %s"""
        values = [record_id, user_id]
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0  # 返回是否真删了（用于权限校验）
    finally:
        conn.close()

def update_record(record_id, user_id, amount, type_chinese, category, date_val, description):
    type_map = {"收入": "income", "支出": "expense"}
    type_english = type_map.get(type_chinese, "expense")
    conn = pymysql.connect(**Wa_config)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    try:
        sql = """update account set amount = %s,type = %s,category = %s,date = %s,description = %s where id = %s and user_id = %s"""
        values = [amount,type_english,category,date_val,description,record_id,user_id]
        cursor.execute(sql, values)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()

def get_all_records(user_id):
    conn = pymysql.connect(**Wa_config)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    try:
        sql = """select id,amount,type,category,date,description from account where user_id = %s order by date desc"""
        values = [user_id]
        cursor.execute(sql,values)
        return cursor.fetchall()
    finally:
        conn.close()

def get_records_by_date(user_id, search_date):
    conn = pymysql.connect(**Wa_config)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        sql = """SELECT id, amount, type, category, date, description 
                 FROM account 
                 WHERE user_id = %s AND date = %s 
                 ORDER BY date DESC"""
        cursor.execute(sql, (user_id, search_date))
        return cursor.fetchall()
    finally:
        conn.close()