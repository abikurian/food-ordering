# backend/config.py
import pymysql
from flask import g

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'food_ordering',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_connection():
    conn = pymysql.connect(**DB_CONFIG)
    return conn
