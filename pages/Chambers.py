import streamlit as st
import os
import pandas as pd
from connect import *

#Function to check if a room is reserved
def is_reserved(chambre):
    reserv = pd.read_sql_query("SELECT CHCODE FROM CHAMBRE WHERE CHCODE IN (SELECT CHCODE FROM RESERVER)", con=engine)
    if chambre in reserv['CHCODE']:
        return True
    return False

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

st.title("Chambers")

#Making the sidebar filter module.
filter = {
    "type" : None,
    "equi" : None,
    "espaces" : None
}

Resultat = pd.DataFrame(None)
with st.sidebar:
    st.title("Filter")
    filter['type'] = st.radio("Types", ['Simple', 'Double', 'Triple', 'Suite', 'Tous'])
    filter['equi'] = st.multiselect("Equipments", ['Jacuzzi', 'Minibar', 'Balcon'])
    filter['equi'] = ret_tuple(filter['equi'])
    match filter['type']:
        case 'Suite':
            filter['espaces'] = ret_tuple(st.multiselect("Espaces", ["Chamber", "Salle a manger", "Salon"]))
            if len(filter['espaces']) - 5 <= 0:
                Resultat = pd.read_sql_query("SELECT DISTINCT * FROM SUITE", con=engine)
            else:
                Resultat = pd.read_sql_query(f"SELECT DISTINCT SU.CHCODE, ESPACE, EQUIP FROM SUITE SU JOIN ESPACES ES ON SU.CHCODE = ES.CHCODE JOIN EQUIPMENTS EQ ON EQ.CHCODE = ES.CHCODE WHERE ESPACE IN {filter['espaces']}", con=engine)
        case 'Tous':
            if len(filter['equi'])-5 <= 0:
                Resultat = pd.read_sql_query(f"SELECT * FROM CHAMBRE", con=engine)
            else:
                Resultat = pd.read_sql_query(f"SELECT CH.CHCODE, SURFACE, EQUIP FROM CHAMBRE CH JOIN EQUIPMENTS EQ ON CH.CHCODE = EQ.CHCODE WHERE EQUIP IN {filter['equi']}", con=engine)
        case _:
            if len(filter['equi'])-5 <= 0:
                Resultat = pd.read_sql_query(f"SELECT * FROM CHAMBRE WHERE LEFT(CHCODE, 1) LIKE '{filter['type'][0]}%%'", con=engine)
            else:
                print(filter['equi'])
                Resultat = pd.read_sql_query(f"SELECT CH.CHCODE, SURFACE, EQUIP FROM CHAMBRE CH JOIN EQUIPMENTS EQ ON CH.CHCODE = EQ.CHCODE WHERE LEFT(CH.CHCODE, 1) LIKE '{filter['type'][0]}%%' AND EQUIP IN {filter['equi']} AND CH.CHCODE NOT IN (SELECT CHCODE FROM SUITE)", con=engine)

st.dataframe(Resultat)