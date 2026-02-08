import pymysql
from config import Wa_config

conn = pymysql.connect(**Wa_config)
cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

def data_add():
    try:
        sql = """insert into account(id,amount,type,category,date,description) values(%s,%s,%s,%s,%s,%s)"""
        values =











