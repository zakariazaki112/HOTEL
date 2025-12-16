import streamlit as st
import os
from connect import *
from datetime import datetime

st.set_page_config(
    page_title="Chambers",
    layout="wide"
)

count = pd.read_sql_query(f'SELECT COUNT(*) AS TOTAL FROM ROOM', con=engine)["TOTAL"][0]
with st.container(border=True):
        st.title("Rooms")
        st.markdown(f"### {count}")


#Function to check if a room is reserved
def is_reserved(ROOM):
    reserv = pd.read_sql_query("SELECT CodR FROM ROOM WHERE CodR IN (SELECT ROOM_CodR FROM BOOKING)", con=engine)
    if ROOM in reserv['CodR'].values:
        return True
    return False

#Making the sidebar filter module.
filter = {
    "type" : None,
    "equi" : None,
    "kitchen" : None,
    "SPACES_Spaces" : None
}

Resultat = pd.DataFrame(None)
query = 0
with st.sidebar:
    st.title("Filter")
    filter['type'] = st.radio("Types", ['Single', 'Double', 'Triple', 'Suite', 'Tous'])
    filter['kitchen'] = st.checkbox("Kitchen")
    filter['equi'] = st.multiselect("Equipments", ['Jacuzzi', 'Minibar', 'Balcon'])
    total_equi = len(filter['equi'])
    query_kitchen = ""
    
    match filter['type']:
        case 'Suite':
            filter['espaces'] = st.multiselect("Espaces", ["Chamber", "Salle a manger", "Salon"])
            if filter['kitchen'] == True:
                filter['espaces'] = filter['espaces']+["kitchen"]
                
            total_esp = len(filter['espaces'])
            if total_equi == 0 and total_esp == 0:
                query = f"SELECT * FROM ROOM WHERE Type = 'suite'"
            elif total_equi == 0:
                query = f"SELECT CH.CodR FROM ROOM CH JOIN HAS_SPACES ES ON CH.CodR = ES.ROOM_CodR WHERE CH.Type = 'suite' AND CH.CodR NOT IN (SELECT ROOM_CodR FROM HAS_AMENITIES) AND SPACES_Space IN {ret_tuple(filter['espaces'])} GROUP BY CH.CodR HAVING COUNT(DISTINCT SPACES_Space) = {total_esp}"
            elif total_esp == 0:
                query = f"SELECT CH.CodR FROM ROOM CH JOIN HAS_AMENITIES EQ ON CH.CodR = EQ.CodR WHERE CH.Type = 'suite' AND CH.CodR NOT IN (SELECT ROOM_CodR FROM HAS_SPACES) AND AMENITIES_Amenity IN {ret_tuple(filter['equi'])} GROUP BY CH.CodR HAVING COUNT(DISTINCT AMENITIES_Amenity) = {total_equi}"
            else:
                query = f"SELECT CH.CodR FROM ROOM CH JOIN HAS_AMENITIES EQ ON CH.CodR = EQ.CodR JOIN HAS_SPACES ES ON ES.CodR = EQ.CodR WHERE Type = 'suite' AND AMENITIES_Amenity IN {ret_tuple(filter['equi'])} AND SPACES_Space IN {ret_tuple(filter['SPACES_Spaces'])} GROUP BY CH.CodR HAVING COUNT(DISTINCT AMENITIES_Amenity) = {total_equi} AND COUNT(DISTINCT SPACES_Space) = {total_esp}"
        case 'Tous':
            if total_equi == 0:
                query = "SELECT * FROM ROOM"
            else:
                query = f"SELECT CH.CodR FROM ROOM CH JOIN HAS_AMENITIES EQ ON CH.CodR = EQ.ROOM_CodR WHERE AMENITIES_Amenity IN {ret_tuple(filter['equi'])} GROUP BY CH.CodR HAVING COUNT(DISTINCT AMENITIES_Amenity) = {total_equi}"
        case _:
            if total_equi == 0:
                query = f"SELECT * FROM ROOM WHERE Type LIKE '{filter['type'].lower()}'"
            else:
                query = f"SELECT CH.CodR FROM ROOM CH JOIN HAS_AMENITIES EQ ON CH.CodR = EQ.CodR WHERE CH.Type LIKE '{filter['type'].lower()}' AND AMENITIES_Amenity IN {ret_tuple(filter['equi'])} AND CH.CodR NOT IN (SELECT CodR FROM SUITE) GROUP BY CH.CodR HAVING COUNT(DISTINCT EQ.AMENITIES_Amenity) = {total_equi}"

ROOM_BOOKING = []
Resultat = pd.read_sql_query(query, con=engine)
for i in Resultat['CodR']:
     ROOM_BOOKING.append(is_reserved(i))
Resultat['BOOKING'] = ROOM_BOOKING
col1, col2 = st.columns(2)
change = True



st.markdown("""
<style>

.booked {
    background-color: crimson;
    border-radius: 20px;
    text-align:center;
    padding:0;
    width: fit-content;
    font-size: 2dvh;
    margin: 0 0 2vh 0;
}
</style>
""", unsafe_allow_html=True)

with st.container(border=True):
    for i in Resultat.values:
        if change:
            with col1:
                with st.container(border=True):
                    name, res = st.columns([1, 1])
                    name.title(f"Room {i[0]}")
                    name.subheader(f"Floors : {i[1]}")
                    name.markdown(f"### Surface : {i[2]}m<sup>2</sup>", unsafe_allow_html=True)
                    if is_reserved(i[0]):
                        res.title("")
                        res.markdown("<h3 class='booked'>Booked</h3>", unsafe_allow_html=True)

                    st.image(f"assets/{i[0]}.jpeg", use_column_width=True)
                    change = False
        else:
            with col2:
                with st.container(border=True):
                    name, res = st.columns([1, 1])
                    name.title(f"Room {i[0]}")
                    name.subheader(f"Floors : {i[1]}")
                    name.markdown(f"### Surface : {i[2]}m<sup>2</sup>", unsafe_allow_html=True)
                    if is_reserved(i[0]):
                        res.title("")
                        res.markdown("<h3 class='booked'>Booked</h3>", unsafe_allow_html=True)
                    st.image(f"assets/{i[0]}.jpeg", use_column_width=True)
                    change = True
                    

with st.expander(label="# Dataset"):
    st.dataframe(Resultat, use_container_width=True)