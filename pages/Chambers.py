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


# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from connect import *  # Assurez-vous que votre module db.query fonctionne

# # ================== CONFIG ==================
# st.set_page_config(
#     page_title="🛏️ Catalogue des Chambres",
#     page_icon="🛏️",
#     layout="wide"
# )

# # ================== STYLE ==================
# st.markdown("""
# <style>
# body { background: linear-gradient(180deg, #F1F8E9, #FFFFFF); }
# h1,h2,h3 { color: #1B5E20; font-weight: 800; }
# .hero-title { font-size: 46px; font-weight: 900; color: #1B5E20; }
# .hero-subtitle { font-size: 20px; color: #388E3C; }
# div[data-testid="metric-container"] { background: linear-gradient(135deg, #FFFFFF, #E8F5E9); border-radius: 20px; padding: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); transition: transform 0.3s ease; }
# div[data-testid="metric-container"]:hover { transform: scale(1.05); }
# .card { background: white; padding: 30px; border-radius: 22px; box-shadow: 0 12px 30px rgba(0,0,0,0.1); text-align: center; transition: all 0.3s ease; margin-bottom: 25px; }
# .card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.15); }
# .stButton > button { background: linear-gradient(135deg, #1B5E20, #4CAF50) !important; color: white !important; border-radius: 14px !important; font-weight: 700 !important; border: none !important; }
# section[data-testid="stSidebar"] { background: linear-gradient(180deg, #E8F5E9, #C8E6C9); }
# [data-testid="stDataFrame"] { border-radius: 15px; border: 1px solid #c8e6c9; }
# .filter-panel { background: linear-gradient(135deg, #E8F5E9, #C8E6C9); padding: 25px; border-radius: 20px; margin-bottom: 30px; border: 2px solid #A5D6A7; }
# footer { visibility: hidden; }
# </style>
# """, unsafe_allow_html=True)

# # ================== HERO ==================
# st.markdown("<div class='hero-title'>🛏️ Catalogue des Chambres & Suites</div>", unsafe_allow_html=True)
# st.markdown("<div class='hero-subtitle'>Explorez notre collection complète d'hébergements</div>", unsafe_allow_html=True)
# st.divider()

# # ================== FILTRES ==================
# st.markdown("<div class='filter-panel'>", unsafe_allow_html=True)
# st.subheader("🔍 Options de recherche")

# filter_col1, filter_col2, filter_col3 = st.columns(3)

# with filter_col1:
#     type_chambre = st.multiselect(
#         "**Type d'hébergement**",
#         ["single", "double", "suite"],
#         default=["single", "double", "suite"],
#         help="Sélectionnez le type de chambre"
#     )

# with filter_col2:
#     surface_min, surface_max = st.slider(
#         "**Surface (m²)**",
#         min_value=10,
#         max_value=100,
#         value=(15, 50),
#         step=1,
#         help="Définissez la plage de surface souhaitée"
#     )

# with filter_col3:
#     try:
#         etage_options = query("SELECT DISTINCT Floor FROM ROOM ORDER BY Floor")
#         if not etage_options.empty:
#             etages = st.multiselect(
#                 "**Étage**",
#                 etage_options['Floor'].tolist(),
#                 default=etage_options['Floor'].tolist()
#             )
#         else:
#             etages = []
#     except:
#         etages = []

# st.markdown("</div>", unsafe_allow_html=True)

# # ================== REQUÊTE SQL ==================
# sql_parts = ["SELECT CodR as code_chambre, SurfaceArea, Floor, Type FROM ROOM WHERE 1=1"]

# if type_chambre:
#     type_list = ",".join(f"'{t}'" for t in type_chambre)
#     sql_parts.append(f" AND Type IN ({type_list})")

# sql_parts.append(f" AND SurfaceArea BETWEEN {surface_min} AND {surface_max}")

# if etages:
#     etages_str = ",".join(str(e) for e in etages)
#     sql_parts.append(f" AND Floor IN ({etages_str})")

# sql_parts.append(" ORDER BY CodR")
# sql = " ".join(sql_parts)

# # ================== EXÉCUTION ==================
# try:
#     df = query(sql)
#     if df is None or not isinstance(df, pd.DataFrame):
#         df = pd.DataFrame()
# except Exception as e:
#     st.error(f"❌ Erreur lors de l'exécution de la requête: {str(e)}")
#     df = pd.DataFrame()

# # ================== AFFICHAGE ==================
# if not df.empty:
#     # ---------- KPI ----------
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     col1, col2, col3, col4 = st.columns(4)

#     col1.metric("🛏️ Chambres trouvées", len(df))
#     col2.metric("👑 Suites", len(df[df["Type"]=="suite"]))
#     col3.metric("📐 Surface moyenne", f"{df['SurfaceArea'].mean():.1f} m²")
#     col4.metric("🏢 Étages différents", df["Floor"].nunique())
#     st.markdown("</div>", unsafe_allow_html=True)

#     # ---------- TABLEAU ----------
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     st.subheader("📋 Liste détaillée des chambres")
#     df_display = df.copy()
#     df_display.columns = ["Code", "Surface (m²)", "Étage", "Type"]
#     st.dataframe(df_display, use_container_width=True, hide_index=True)

#     export_col1, export_col2 = st.columns(2)
#     with export_col1:
#         st.download_button(
#             "📥 Télécharger en CSV",
#             df_display.to_csv(index=False),
#             file_name="chambres.csv",
#             mime="text/csv",
#             use_container_width=True
#         )
#     with export_col2:
#         if st.button("🔄 Actualiser l'affichage", use_container_width=True):
#             st.rerun()
#     st.markdown("</div>", unsafe_allow_html=True)

#     # ---------- VISUALISATIONS ----------
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     st.subheader("📊 Analyses visuelles")

#     viz_tab1, viz_tab2, viz_tab3 = st.tabs(["📈 Par type", "📊 Par étage", "📐 Distribution surface"])

#     with viz_tab1:
#         type_dist = df["Type"].value_counts()
#         st.bar_chart(type_dist)
#         st.caption("Répartition des hébergements par type")

#     with viz_tab2:
#         etage_dist = df.groupby("Floor").size()
#         st.line_chart(etage_dist)
#         st.caption("Nombre de chambres par étage")

#     with viz_tab3:
#         fig, ax = plt.subplots(figsize=(10,4))
#         ax.hist(df["SurfaceArea"], bins=10, color='#4CAF50', edgecolor='black', alpha=0.7)
#         ax.set_xlabel("Surface (m²)")
#         ax.set_ylabel("Nombre de chambres")
#         ax.set_title("Distribution des surfaces")
#         ax.grid(True, alpha=0.3)
#         st.pyplot(fig)

#     st.markdown("</div>", unsafe_allow_html=True)

#     # ---------- RECHERCHE RAPIDE ----------
#     st.markdown("<div class='card'>", unsafe_allow_html=True)
#     st.subheader("🔍 Recherche rapide par code")
#     search_col1, search_col2 = st.columns([3,1])
#     with search_col1:
#         code_search = st.text_input("Entrez le code d'une chambre:", placeholder="Ex: 1, 2...")

#     with search_col2:
#         search_btn = st.button("🔎 Rechercher", use_container_width=True)

#     if search_btn and code_search:
#         try:
#             code_int = int(code_search)
#             result = df[df["code_chambre"] == code_int]
#             if not result.empty:
#                 st.success(f"✅ Chambre {code_int} trouvée!")
#                 st.dataframe(result, use_container_width=True)
#             else:
#                 sql_single = f"SELECT CodR as code_chambre, SurfaceArea, Floor, Type FROM ROOM WHERE CodR = {code_int}"
#                 single_result = query(sql_single)
#                 if not single_result.empty:
#                     st.success(f"✅ Chambre {code_int} trouvée dans la base!")
#                     st.dataframe(single_result, use_container_width=True)
#                 else:
#                     st.warning(f"❌ Aucune chambre avec le code {code_int}")
#         except ValueError:
#             st.error("⚠️ Veuillez entrer un code numérique valide")
#     st.markdown("</div>", unsafe_allow_html=True)

# else:
#     st.markdown("<div class='card' style='background: #FFF3E0;'>", unsafe_allow_html=True)
#     st.warning("⚠️ Aucune chambre ne correspond aux critères de recherche.")
#     st.info("💡 Essayez d'élargir vos filtres de recherche.")
#     st.markdown("</div>", unsafe_allow_html=True)

# # ================== SIDEBAR ==================
# with st.sidebar:
#     st.header("⚙️ Paramètres")
#     if st.button("🔄 Réinitialiser tous les filtres", use_container_width=True):
#         st.rerun()
#     st.divider()
#     with st.expander("📖 Détails techniques"):
#         st.write("**Requête SQL exécutée:**")
#         st.code(sql, language="sql")
#         if not df.empty:
#             st.write(f"**Résultats:** {len(df)} ligne(s)")
#         st.write("**Table utilisée:** ROOM")
#     st.divider()
#     if st.button("🔌 Tester la connexion BD", use_container_width=True):
#         try:
#             test_result = query("SELECT COUNT(*) as total FROM ROOM")
#             st.success(f"✅ Connecté - {test_result.iloc[0,0]} chambres")
#         except Exception as e:
#             st.error(f"❌ Erreur: {str(e)}")
#     st.caption("🛏️ Catalogue Chambres")

# # ================== FOOTER ==================
# st.divider()
# st.caption("🏨 Hôtel Management System • Catalogue des Chambres • © 2024")