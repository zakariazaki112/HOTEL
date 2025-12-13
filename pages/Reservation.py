import streamlit as st
from connect import *


st.title("Reservations")
donnee = {
    "Nom" : None,
    "Prenom" : None,
    "Email" : None,
    "Type" : None,
    "Date_D" : None,
    "Date_F" : None
}

def print_info(inf):
    for (k, v)in inf.items():
        st.write(f"{k} : {v}")

def check_data(conn):
    exists = conn.execute(text(f"SELECT CHCODE FROM CHAMBRE WHERE TYPE LIKE '{donnee['Type'].upper()}' AND CHCODE NOT IN (SELECT CHCODE FROM RESERVER)"))
    if exists.all() == []:
        return False;
    exists = conn.execute(text(f"SELECT CHCODE FROM CHAMBRE WHERE TYPE LIKE '{donnee['Type'].upper()}' AND CHCODE NOT IN (SELECT CHCODE FROM RESERVER)"))
    return exists

donnee["Type"] = st.selectbox("Type", ['Simple', 'Double', 'Triple', 'Suite'])
with st.form(key="res"):
    donnee["Nom"] = st.text_input(label="Nom")
    donnee["Prenom"] = st.text_input(label="Prenom")
    donnee["Email"] = st.text_input(label="Email")
    
   
    if donnee['Type'] == "Suite":
        st.multiselect("Equipments", ["Jacuzzi", "Minibar", "Balcon"])
    
    donnee["Date_D"] = st.date_input(label="Date de Debut")
    donnee["Date_F"] = st.date_input(label="Date Final")
    sub = st.form_submit_button(label="Reserver")
    if sub:
        if not all(donnee.values()):
            st.warning("All cases need to be filled")
        else:
            if donnee["Date_D"] == donnee["Date_F"]:
                st.warning("Start and Final Dates can't be the same")
            else:
                with engine.connect() as conn:
                    data = check_data(conn)
                    available_ID = 0
                    if data != False:
                        available_ID = data.all()[0][0]
                        conn.execute(text(f"INSERT INTO RESERVER(CHCODE, TYPE, DATE_RESERVER, DATE_END) VALUES('{available_ID}', '{donnee['Type']}', '{donnee['Date_D']}' ,'{donnee['Date_F']}')"))
                        conn.commit()
                        st.success("Your reservation has been submited successfully")
                    else:
                        st.warning("Sorry, no rooms are available right now")