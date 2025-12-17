from connect import *


st.set_page_config(
    page_title="Chambers",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ======Functions=======


def type_count(type):
    return pd.read_sql_query(f"SELECT COUNT(*) FROM ROOM WHERE Type = '{type}'", con=engine).iloc[0, 0]

# Function to check if a room is reserved


def is_reserved(ROOM):
    reserv = pd.read_sql_query(
        "SELECT CodR FROM ROOM WHERE CodR IN (SELECT ROOM_CodR FROM BOOKING)", con=engine)
    if ROOM in reserv['CodR'].values:
        return True
    return False


# =====Styles======
st.markdown("""
            <style>
                h1, h2, h3{
                    scale: 0.7;
                    padding: 0;
                }
                img{
                    padding: 1rem;
                }
                [data-testid='stMetric']{
                    background-color: rgba(41, 44, 50, 0.5);
                    border-radius: 10px;
                    padding: 1rem;
                }
                .booked {
                    background-color: crimson;
                    border-radius: 20px;
                    text-align: center;
                    width: fit-content;
                    font-size: 2dvh;
                    padding: 0.5rem;
                    margin: 0 0 2vh 0;
                }
            """, unsafe_allow_html=True)

# =====Types total======
room_count = pd.read_sql_query(
    f'SELECT COUNT(*) AS TOTAL FROM ROOM', con=engine).iloc[0, 0]
simple, double, triple, suite = st.columns(4)

st.metric("Rooms", f"{room_count}")

with st.container(border=True):
    with simple:
        st.metric("Simple", type_count('single'))
    with double:
        st.metric("Double", type_count('double'))
    with triple:
        st.metric("Triple", type_count('triple'))
    with suite:
        st.metric("Suite", type_count('suite'))


# Making the sidebar filter module.
filter = {
    "type": None,
    "equi": None,
    "kitchen": None,
    "SPACES_Spaces": None
}

Resultat = pd.DataFrame(None)
query = 0
with st.sidebar:
    st.title("Filter")
    filter['type'] = st.radio(
        "Types", ['Single', 'Double', 'Triple', 'Suite', 'Tous'])

    filter['equi'] = st.multiselect(
        "Equipments", ['Jacuzzi', 'Minibar', 'Balcon'])
    total_equi = len(filter['equi'])

    match filter['type']:
        case 'Suite':
            filter['kitchen'] = st.checkbox("Kitchen")
            filter['espaces'] = st.multiselect(
                "Espaces", ["Chamber", "Salle a manger", "Salon"])
            if filter['kitchen'] == True:
                filter['espaces'] = filter['espaces']+["kitchen"]

            total_esp = len(filter['espaces'])
            if total_equi == 0 and total_esp == 0:
                query = f"SELECT * FROM ROOM WHERE Type = 'suite'"
            elif total_equi == 0:
                query = f"SELECT CH.CodR, CH.Floor, CH.SurfaceArea  FROM ROOM CH JOIN HAS_SPACES ES ON CH.CodR = ES.ROOM_CodR WHERE CH.Type = 'suite' AND CH.CodR NOT IN (SELECT ROOM_CodR FROM HAS_AMENITIES) AND SPACES_Space IN {ret_tuple(filter['espaces'])} GROUP BY CH.CodR HAVING COUNT(DISTINCT SPACES_Space) = {total_esp}"
            elif total_esp == 0:
                query = f"SELECT CH.CodR, CH.Floor, CH.SurfaceArea FROM ROOM CH JOIN HAS_AMENITIES EQ ON CH.CodR = EQ.ROOM_CodR WHERE CH.Type = 'suite' AND CH.CodR NOT IN (SELECT ROOM_CodR FROM HAS_SPACES) AND AMENITIES_Amenity IN {ret_tuple(filter['equi'])} GROUP BY CH.CodR HAVING COUNT(DISTINCT AMENITIES_Amenity) = {total_equi}"
            else:
                query = f"SELECT CH.CodR, CH.Floor, CH.SurfaceArea FROM ROOM CH JOIN HAS_AMENITIES EQ ON CH.CodR = EQ.ROOM_CodR JOIN HAS_SPACES ES ON ES.CodR = EQ.CodR WHERE Type = 'suite' AND AMENITIES_Amenity IN {ret_tuple(filter['equi'])} AND SPACES_Space IN {ret_tuple(filter['SPACES_Spaces'])} GROUP BY CH.CodR HAVING COUNT(DISTINCT AMENITIES_Amenity) = {total_equi} AND COUNT(DISTINCT SPACES_Space) = {total_esp}"
        case 'Tous':
            if total_equi == 0:
                query = "SELECT * FROM ROOM"
            else:
                query = f"SELECT CH.CodR, CH.Floor, CH.SurfaceArea FROM ROOM CH JOIN HAS_AMENITIES EQ ON CH.CodR = EQ.ROOM_CodR WHERE AMENITIES_Amenity IN {ret_tuple(filter['equi'])} GROUP BY CH.CodR HAVING COUNT(DISTINCT AMENITIES_Amenity) = {total_equi}"
        case _:
            if total_equi == 0:
                query = f"SELECT * FROM ROOM WHERE Type LIKE '{filter['type'].lower()}'"
            else:
                query = f"SELECT CH.CodR, CH.Floor, CH.SurfaceArea FROM ROOM CH JOIN HAS_AMENITIES EQ ON CH.CodR = EQ.ROOM_CodR WHERE CH.Type LIKE '{filter['type'].lower()}' AND AMENITIES_Amenity IN {ret_tuple(filter['equi'])} GROUP BY CH.CodR HAVING COUNT(DISTINCT EQ.AMENITIES_Amenity) = {total_equi}"


ROOM_BOOKING = []
Resultat = pd.read_sql_query(query, con=engine)
for i in Resultat['CodR']:
    ROOM_BOOKING.append(is_reserved(i))
Resultat['BOOKING'] = ROOM_BOOKING
col1, col2 = st.columns(2)
change = True
with st.container(border=False):
    for i in Resultat.values:
        if change:
            with col1:
                with st.container(border=True):
                    name, res = st.columns(2)
                    name.header(f"Room {i[0]}")
                    name.subheader(f"Floor: {i[1]}")
                    name.markdown(
                        f"### Surface : {i[2]}m<sup>2</sup>", unsafe_allow_html=True)
                    if is_reserved(i[0]):
                        res.title("")
                        res.markdown("<h3 class='booked'>Booked</h3>",
                                     unsafe_allow_html=True)

                    st.image(f"assets/{i[0]}.jpeg")
                    change = False
        else:
            with col2:
                with st.container(border=True):
                    name, res = st.columns(2)
                    name.header(f"Room {i[0]}")
                    name.subheader(f"Floor: {i[1]}")
                    name.markdown(
                        f"### Surface : {i[2]}m<sup>2</sup>", unsafe_allow_html=True)
                    if is_reserved(i[0]):
                        res.title("")
                        res.markdown("<h3 class='booked'>Booked</h3>",
                                     unsafe_allow_html=True)
                    st.image(f"assets/{i[0]}.jpeg")
                    change = True


with st.expander(label="# Dataset"):
    st.dataframe(Resultat, use_container_width=True)
