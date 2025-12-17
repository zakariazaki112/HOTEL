#asma
from sqlalchemy import create_engine, text
import streamlit as st
import pandas as pd
import os
def ret_tuple(arr):
    if len(arr) == 0:
        return "(' ')"
    output = '('
    k = 0
    for i in arr:
        if k != len(arr)-1:
            output += f"'{i}'"+','
        else:
            output += f"'{i}'"
        k += 1
    output += ')'
    return output

def query(sql):
    return pd.read_sql(sql, con=engine)

USER = os.getenv("DB_USER", "root")
PASS = os.getenv("DB_PASS", "Thi$i$myp4ss")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "3306")
DB = os.getenv("DB_NAME", "hotel")
engine_url = f"mysql+pymysql://{USER}:{PASS}@{HOST}:{PORT}/{DB}?charset=utf8mb4"
engine = create_engine(engine_url)
