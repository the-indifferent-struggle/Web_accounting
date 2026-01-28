from flask import Flask,render_template,request
from config import Wa_config
import pymysql

conn = pymysql.connect(**Wa_config)
cursor = conn.cursor(cursor = pymysql.cursor.DictCursor)