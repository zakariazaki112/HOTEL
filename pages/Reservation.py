import streamlit as st
from connect import *


st.title("Reservations")
donnee = {
    "Nom" : None,
    "Prenom" : None,
    "Email" : None,
    "Type" : None,
    "Date_D" : None,
    "Date_F" : None,
    "Espace" : None,
    "Equipment" : None,
    "Agence" : None
}

def print_info(inf):
    for (k, v)in inf.items():
        st.write(f"{k} : {v}")

def check_data(conn, total_equi, total_esp=0):
    if total_equi == 0:
        query = f"SELECT CHCODE FROM CHAMBRE WHERE CHCODE LIKE '{donnee['Type'][0]}%%' AND CHCODE NOT IN (SELECT CHCODE FROM RESERVER)"
    else:
        query = f"SELECT CH.CHCODE FROM CHAMBRE CH JOIN HAS_EQUIPMENTS EQ ON CH.CHCODE = EQ.CHCODE WHERE CH.CHCODE LIKE '{donnee['Type'][0]}%%' AND CH.CHCODE NOT IN (SELECT CHCODE FROM RESERVER) AND EQUIP IN {ret_tuple(donnee['Equipment'])} GROUP BY CH.CHCODE HAVING COUNT(DISTINCT EQUIP) = {total_equi}"
        
    if donnee["Type"] == "Suite":
        if total_equi == 0 and total_esp == 0:
            query = f"SELECT DISTINCT CHCODE FROM CHAMBRE WHERE CHCODE LIKE 'V%%' AND CHCODE NOT IN (SELECT CHCODE FROM RESERVER) AND CHCODE NOT IN (SELECT CHCODE FROM HAS_EQUIPMENTS) AND CHCODE NOT IN (SELECT CHCODE FROM HAS_ESPACES)"
        elif total_equi == 0:
            query = f"SELECT CH.CHCODE FROM CHAMBRE CH JOIN HAS_ESPACES ES ON CH.CHCODE = ES.CHCODE WHERE CH.CHCODE LIKE 'V%%' AND CH.CHCODE NOT IN (SELECT CHCODE FROM RESERVER) AND CH.CHCODE NOT IN (SELECT CHCODE FROM HAS_EQUIPMENTS) AND ESPACE IN {ret_tuple(donnee['Espace'])} GROUP BY CH.CHCODE HAVING COUNT(DISTINCT ESPACE) = {total_esp}"
        elif total_esp == 0:
            query = f"SELECT CH.CHCODE FROM CHAMBRE CH JOIN HAS_EQUIPMENTS EQ ON CH.CHCODE = EQ.CHCODE WHERE CH.CHCODE LIKE 'V%%' AND CH.CHCODE NOT IN (SELECT CHCODE FROM RESERVER) AND CH.CHCODE NOT IN (SELECT CHCODE FROM HAS_ESPACES) AND EQUIP IN {ret_tuple(donnee['Equipment'])} GROUP BY CH.CHCODE HAVING COUNT(DISTINCT EQUIP) = {total_equi}"
        else:
            query = f"SELECT CH.CHCODE FROM CHAMBRE CH JOIN HAS_EQUIPMENTS EQ ON CH.CHCODE = EQ.CHCODE JOIN HAS_ESPACES ES ON ES.CHCODE = EQ.CHCODE WHERE CH.CHCODE LIKE 'V%%' AND CH.CHCODE NOT IN (SELECT CHCODE FROM RESERVER) AND EQUIP IN {ret_tuple(donnee['Equipment'])} AND ESPACE IN {ret_tuple(donnee['Espace'])} GROUP BY CH.CHCODE HAVING COUNT(DISTINCT EQUIP) = {total_equi} AND COUNT(DISTINCT ESPACE) = {total_esp}"
    exists = pd.read_sql_query(query, con=conn)
    return exists


        
donnee["Type"] = st.selectbox("Type", ['Simple', 'Double', 'Triple', 'Suite'])

with st.form(key="res"):
    donnee["Nom"] = st.text_input(label="Nom")
    donnee["Prenom"] = st.text_input(label="Prenom")
    donnee["Email"] = st.text_input(label="Email")
    agences = pd.read_sql_query("SELECT DISTINCT NOM FROM AGENCE", con=engine)
    donnee["Agence"] = st.selectbox("Agences", agences)
    donnee["Equipment"] = st.multiselect("Equipments", ['Jacuzzi', 'Minibar', 'Balcon'])
    if donnee['Type'] == "Suite":
        donnee["Espace"] = st.multiselect("Espaces", ["Chamber", "Salle a manger", "Salon"])
    
    donnee["Date_D"] = st.date_input(label="Date de Debut")
    donnee["Date_F"] = st.date_input(label="Date Final")
    
    sub = st.form_submit_button(label="Reserver")
    if sub:
        if donnee["Date_D"] == donnee["Date_F"]:
            st.warning("Start and Final Dates can't be the same")
        elif donnee["Date_D"] > donnee["Date_F"]:
            st.warning("Trying to go back to the past now are we?")
        else:
            with engine.connect() as conn:
                try:
                     data = check_data(conn, len(donnee["Equipment"]), len(donnee["Espace"]))
                except:
                    data = check_data(conn, len(donnee["Equipment"]))
                    available_ID = 0
                    if not data.empty:
                        available_ID = data['CHCODE'][0]
                        agency_id = pd.read_sql_query(f"SELECT ACODE FROM AGENCE WHERE NOM LIKE '{donnee['Agence']}'", con=engine)['ACODE'][0]
                        conn.execute(text(f"INSERT INTO RESERVER(CHCODE, DATE_DEBUT, DATE_END, PRIX, AGENCE) VALUES('{available_ID}', '{donnee['Date_D']}' ,'{donnee['Date_F']}', 999, '{agency_id}')"))
                        conn.commit()
                        st.success(f"Your reservation has been submited successfully, The room ID is : {available_ID}")
                    else:
                        st.warning("Sorry, no rooms are available right now")