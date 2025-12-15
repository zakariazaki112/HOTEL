import streamlit as st
from connect import *

#This is the landing page
#This is a test comment
tables = {'CHAMBRE' : 0, 'AGENCE': 0}
for (tab, val) in tables.items() :
    count = pd.read_sql_query(f'SELECT COUNT(*) AS TOTAL FROM {tab}', con=engine)
    tables[tab] = count['TOTAL'][0]


st.set_page_config(
    page_title="Hotel dashboard",
    layout="wide"
)

st.status("The status", state="error")

st.markdown("# Hotel Dashboard ")
Agen, Cham = st.columns(2)

with st.container(border=False):
    with Agen:
        with st.container(border=True):
            st.title("Agences")
            st.header(tables['AGENCE'])
    with Cham:
        with st.container(border=True):
            st.title("Chambers")
            st.header(tables["CHAMBRE"])
st.header("Made by : ")
st.markdown("* Test1\n* Test2\n* Test3\n* Test4\n* Test5\n* Test6")