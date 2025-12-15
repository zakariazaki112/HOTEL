#asma
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import streamlit as st
import pandas as pd

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

chamber_count = 0;
agency_count = 0;
user_count = 0;

dialect = 'mysql'
username = 'root'
password = 'Thi$i$myp4ss'
host = "localhost"
#host = "host.docker.internal"
dbname = 'HOTEL'

engine = create_engine(f"{dialect}://{username}:{password}@{host}/{dbname}")
