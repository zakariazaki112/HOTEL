from connect import *

# ================== CONFIG ==================
st.set_page_config(
    page_title="Agences",
    page_icon="📍",
    layout="wide"
)

# ================== STYLE ==================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #0e1117; }
h1, h2, h3 { color: white; font-weight: 800; }
div[data-testid="metric-container"] { 
    background: linear-gradient(135deg, #FFFFFF, #E8F5E9);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ================== HERO ==================
st.title("📍 Gestion des Agences de Voyage")
st.divider()

# ================== METRICS ==================
col1, col2, col3 = st.columns(3)

try:
    nb_agences = query("SELECT COUNT(*) FROM TRAVEL_AGENCY").iloc[0, 0]
    nb_villes = query("SELECT COUNT(DISTINCT City_Address) FROM TRAVEL_AGENCY").iloc[0, 0]

    ville_top = query("""
        SELECT City_Address, COUNT(*) as count 
        FROM TRAVEL_AGENCY 
        GROUP BY City_Address 
        ORDER BY count DESC 
        LIMIT 1
    """).iloc[0, 0]

except:
    nb_agences = nb_villes = 0
    ville_top = "N/A"

col1.metric("🏢 Agences", nb_agences)
col2.metric("🌍 Villes", nb_villes)
col3.metric("🏆 Ville active", ville_top)

st.divider()

# ================== CARTE ==================
st.subheader("🗺️ Carte des agences")

try:
    # Jointure avec CITY pour obtenir latitude et longitude
    map_data = query("""
        SELECT C.Latitude as lat, C.Longitude as lon
        FROM TRAVEL_AGENCY A
        JOIN CITY C ON A.City_Address = C.Name
    """)

    if not map_data.empty:
        st.map(map_data)
    else:
        st.info("Aucune donnée géographique disponible")
except:
    st.info("Impossible d'afficher la carte")

# ================== LISTE ==================
st.subheader("📋 Liste des agences")

try:
    # Liste des villes
    villes = query("SELECT DISTINCT City_Address FROM TRAVEL_AGENCY ORDER BY City_Address")
    ville_choisie = st.selectbox(
        "Filtrer par ville:",
        ["Toutes les villes"] + villes['City_Address'].tolist()
    )

    if ville_choisie != "Toutes les villes":
        df = query(f"""
            SELECT 
                CodA as "Code",
                WebSite as "Site web",
                Tel as "Téléphone",
                CONCAT(Street_Address, ' ', Num_Address, ', ', ZIP_Address, ' ', City_Address, ', ', Country_Address) as "Adresse"
            FROM TRAVEL_AGENCY 
            WHERE City_Address = '{ville_choisie}'
            ORDER BY CodA
        """)
    else:
        df = query("""
            SELECT 
                CodA as "Code",
                WebSite as "Site web",
                Tel as "Téléphone",
                CONCAT(Street_Address, ' ', Num_Address, ', ', ZIP_Address, ' ', City_Address, ', ', Country_Address) as "Adresse"
            FROM TRAVEL_AGENCY 
            ORDER BY CodA
        """)

    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(e)
    st.warning("Impossible de charger les données")

st.divider()
st.caption("📍 Module Agences • Base: hotel")