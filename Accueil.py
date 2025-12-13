import streamlit as st
import os
import pathlib
from connect import *

#This is the landing page

tables = {'CHAMBRE' : 0, 'AGENCE': 0}
with engine.connect() as conn:
    for (tab, val) in tables.items() :
        sql=text(f'SELECT * FROM {tab}')
        results = conn.execute(sql)
        for res in results:
            tables[tab]+= 1


# st.set_page_config(
#     page_title="Hotel dashboard",
#     layout="wide"
# )


st.title("Hotel")

st.subheader("A humble hotel situated on the outskirts of nowhere")
Agen, Cham, Users = st.columns(3)

with st.container(border=False, key="metrics"):
    with Agen:
        with st.container(border=False):
            st.header("Agences")
            st.subheader(tables['AGENCE'])
    with Cham:
        with st.container(border=False):
            st.header("Chambers")
            st.subheader(tables["CHAMBRE"])
    with Users:
        with st.container(border=False):
            st.header("Users")
            st.subheader(user_count)
st.header("Made by : ")
st.markdown("* Test1\n* Test2\n* Test3\n* Test4\n* Test5\n* Test6")


conn.close()
