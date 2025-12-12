import streamlit as st
import os
import pandas as pd
from connect import *


def create_box(Title, Desc, parametre, img):
    with st.container(border=True):
        if(parametre != ""):
            st.subheader(parametre)
        st.header(Title)
        st.write(Desc)
        st.image(os.path.join(os.getcwd(), "static", img))
    
def is_reserved(chambre):
    with engine.connect() as conn:
        reserv = conn.execute(text(f"SELECT CHCODE FROM CHAMBRE WHERE CHCODE IN (SELECT CHCODE FROM RESERVER)"))
        reserv = [element for list_tuples in reserv.all() for element in list_tuples]
        if chambre in reserv:
            return True
        return False

filter = {
    "type" : None,
    "kitchen" : None,
    "equi" : None,
}

st.title("Chambers")
#Page sidebat

#Adding filter options to the sidebar
with st.sidebar:
    st.sidebar.title("Filter")
    filter['type'] = st.sidebar.radio("Type", ["Simple", "Double", "Triple", "Suite", "Tous"])
    filter['kitchen'] = st.sidebar.checkbox("Kitchen")
    if filter['type'] == 'Suite':
        eq = ["Jacuzzi", "Minibar", "Balcon"]
        filter['equi'] = st.sidebar.multiselect("Equipment pour les suites", eq)
        for i in range(len(eq)-len(filter['equi'])):
            filter["equi"].insert(i,'')
    
#Getting the available rooms depending on the filter
res = ()      
with engine.connect() as conn:
    if(filter['type'] == 'Tous'):
        res = pd.read_sql_query(f"SELECT * FROM CHAMBRE WHERE HAS_CUISINE = '{filter['kitchen']}'", con=engine)
    elif(filter['type'] == 'Suite' and any(filter['equi'])):
        res = pd.read_sql_query(f"SELECT CH.CHCODE, EQUIP, ETAGE, SUPERFICIE, TYPE, HAS_CUISINE FROM EQUIPMENTS SU JOIN CHAMBRE CH ON SU.CHCODE = CH.CHCODE WHERE HAS_CUISINE = '{filter['kitchen']}' AND EQUIP IN ('{filter['equi'][0].lower()}','{filter['equi'][1].lower()}','{filter['equi'][2].lower()}')", con=engine)
    else:
        res = pd.read_sql_query(f"SELECT * FROM CHAMBRE WHERE TYPE = '{filter['type']}' AND HAS_CUISINE = '{filter['kitchen']}'", con=engine)

for i in res['CHCODE']:
    
    res["Reserver"] = is_reserved(i)
print(res['Reserver'])
st.dataframe(res)