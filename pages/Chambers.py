import streamlit as st
import os
from connect import *
from datetime import datetime

def date_ended(DATE):
    return 
    #engine.connect().execute(text(f"DELETE FROM RESERVER WHERE DATE_END='{DATE}'"))
    #engine.connect().commit()

current_date = str(datetime.now().strftime("%Y-%m-%d 00:00:00"))
reservation_dates = pd.read_sql_query("SELECT CHCODE, DATE_END FROM RESERVER", con=engine)
with st.status("Room status"):
    for (ch, date) in reservation_dates.values:
        if str(date) == current_date:
            date_ended(current_date)
            st.warning(f"Reservation date ended for {ch}")

#Function to check if a room is reserved
def is_reserved(chambre):
    reserv = pd.read_sql_query("SELECT CHCODE FROM CHAMBRE WHERE CHCODE IN (SELECT CHCODE FROM RESERVER)", con=engine)
    if chambre in reserv['CHCODE'].values:
        return True
    return False



st.title("Chambers")

#Making the sidebar filter module.
filter = {
    "type" : None,
    "equi" : None,
    "espaces" : None
}

Resultat = pd.DataFrame(None)
query = 0
with st.sidebar:
    st.title("Filter")
    filter['type'] = st.radio("Types", ['Simple', 'Double', 'Triple', 'Suite', 'Tous'])
    filter['equi'] = st.multiselect("Equipments", ['Jacuzzi', 'Minibar', 'Balcon'])
    total_equi = len(filter['equi'])
    
    match filter['type']:
        case 'Suite':
            filter['espaces'] = st.multiselect("Espaces", ["Chamber", "Salle a manger", "Salon"])
            total_esp = len(filter['espaces'])
            if total_equi == 0 and total_esp == 0:
                query = f"SELECT * FROM CHAMBRE WHERE CHCODE LIKE 'V%%'"
            elif total_equi == 0:
                query = f"SELECT CH.CHCODE FROM CHAMBRE CH JOIN HAS_ESPACES ES ON CH.CHCODE = ES.CHCODE WHERE CH.CHCODE LIKE 'V%%' AND CH.CHCODE NOT IN (SELECT CHCODE FROM HAS_EQUIPMENTS) AND ESPACE IN {ret_tuple(filter['espaces'])} GROUP BY CH.CHCODE HAVING COUNT(DISTINCT ESPACE) = {total_esp}"
            elif total_esp == 0:
                query = f"SELECT CH.CHCODE FROM CHAMBRE CH JOIN HAS_EQUIPMENTS EQ ON CH.CHCODE = EQ.CHCODE WHERE CH.CHCODE LIKE 'V%%' AND CH.CHCODE NOT IN (SELECT CHCODE FROM HAS_ESPACES) AND EQUIP IN {ret_tuple(filter['equi'])} GROUP BY CH.CHCODE HAVING COUNT(DISTINCT EQUIP) = {total_equi}"
            else:
                query = f"SELECT CH.CHCODE FROM CHAMBRE CH JOIN HAS_EQUIPMENTS EQ ON CH.CHCODE = EQ.CHCODE JOIN HAS_ESPACES ES ON ES.CHCODE = EQ.CHCODE WHERE CH.CHCODE LIKE 'V%%' AND EQUIP IN {ret_tuple(filter['equi'])} AND ESPACE IN {ret_tuple(filter['espaces'])} GROUP BY CH.CHCODE HAVING COUNT(DISTINCT EQUIP) = {total_equi} AND COUNT(DISTINCT ESPACE) = {total_esp}"
        case 'Tous':
            if total_equi == 0:
                query = "SELECT * FROM CHAMBRE"
            else:
                query = f"SELECT CH.CHCODE FROM CHAMBRE CH JOIN HAS_EQUIPMENTS EQ ON CH.CHCODE = EQ.CHCODE WHERE EQUIP IN {ret_tuple(filter['equi'])} GROUP BY CH.CHCODE HAVING COUNT(DISTINCT EQUIP) = {total_equi}"
        case _:
            if total_equi == 0:
                query = f"SELECT * FROM CHAMBRE WHERE CHCODE LIKE '{filter['type'][0]}%%'"
            else:
                query = f"SELECT CH.CHCODE FROM CHAMBRE CH JOIN HAS_EQUIPMENTS EQ ON CH.CHCODE = EQ.CHCODE WHERE CH.CHCODE LIKE '{filter['type'][0]}%%' AND EQUIP IN {ret_tuple(filter['equi'])} AND CH.CHCODE NOT IN (SELECT CHCODE FROM SUITE) GROUP BY CH.CHCODE HAVING COUNT(DISTINCT EQ.EQUIP) = {total_equi}"

chambre_reserver = []
Resultat = pd.read_sql_query(query, con=engine)
for i in Resultat['CHCODE']:
     chambre_reserver.append(is_reserved(i))
Resultat['Reserver'] = chambre_reserver
with st.expander(label="# Dataset"):
    st.dataframe(Resultat, use_container_width=True)
col1, col2 = st.columns(2)
change = True

with st.container(border=True):
    for i in Resultat['CHCODE']:
        if change:
            with col1:
                with st.container(border=True):
                    name, res = st.columns(2)
                    name.header(i)
                    if is_reserved(i):
                        res.header("Reserver")
                    else:
                        res.header("Pas reserver")
                    st.write("Something cool, I don't know")
                    try:
                        st.image(f"static/fixed-{i}.jpeg")
                    except:
                        st.warning(f"static/fixed-NA.png")
                    change = False
        else:
            with col2:
                with st.container(border=True):
                    name, res = st.columns(2)
                    name.header(i)
                    if is_reserved(i):
                        res.header("Reserver")
                    else:
                        res.header("Pas reserver")
                    
                    st.write("Something cool, I don't know")
                    try:
                        st.image(f"static/fixed-{i}.jpeg")
                    except:
                        st.image(f"static/fixed-NA.png")
                    change = True
                    

