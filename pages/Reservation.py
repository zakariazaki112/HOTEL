import streamlit as st
from connect import *
import calendar
import matplotlib.pyplot as plt
# ================== CONFIG ==================
st.set_page_config(
    page_title="📅 Réservations",
    page_icon="📅",
    layout="wide"
)

# ================== STYLE ==================
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #0e1117;
    }
h1, h2, h3 {
    color: white;
    font-weight: 800;
}
div[data-testid="metric-container"] { 
    background: linear-gradient(135deg, #FFFFFF, #E8F5E9);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ================== HERO ==================
st.title("📅 Gestion des Réservations")
st.divider()

# ================== METRICS ==================
col1, col2, col3 = st.columns(3)

try:
    total = query("SELECT COUNT(*) FROM BOOKING").iloc[0, 0]
    revenu = query("SELECT SUM(Cost) FROM BOOKING").iloc[0, 0]
    prix_moy = query("SELECT AVG(Cost) FROM BOOKING").iloc[0, 0]

    chambre_pop = query("""
        SELECT ROOM_CodR, COUNT(*) as nb_reservations
        FROM BOOKING 
        GROUP BY ROOM_CodR 
        ORDER BY nb_reservations DESC 
        LIMIT 1
    """)

    chambre_top = chambre_pop.iloc[0, 0] if not chambre_pop.empty else "N/A"

except Exception as e:
    print(e)
    total = revenu = prix_moy = 0
    chambre_top = "N/A"

col1.metric("📅 Réservations", total)
col2.metric("💰 Revenu total", f"{revenu:,.0f} €" if revenu else "0 €")
col3.metric("👑 Chambre populaire", chambre_top)

st.divider()

# ================== ANALYSE MENSUELLE ==================
st.subheader("📊 Analyse par mois")

try:
    monthly = query("""
        SELECT 
            MONTH(StartDate) as Mois,
            COUNT(*) as `Nombre de réservations`,
            SUM(Cost) as `Revenu total`,
            AVG(Cost) as `Prix moyen`
        FROM BOOKING
        GROUP BY MONTH(StartDate)
        ORDER BY Mois
    """)

    if not monthly.empty:
        st.dataframe(monthly, use_container_width=True)

        # Graphique
        st.subheader("📈 Évolution des réservations")
        st.line_chart(monthly.set_index('Mois')['Nombre de réservations'])
    else:
        st.info("Aucune donnée mensuelle disponible")

except Exception as e:
    st.warning("Impossible de charger l'analyse mensuelle")

# ================== DERNIÈRES RÉSERVATIONS ==================
st.divider()
st.subheader("📋 Dernières réservations")
recent = 0
try:
    recent = query("""
        SELECT 
            B.ROOM_CodR as Chambre,
            B.StartDate as Début,
            B.EndDate as Fin,
            B.Cost as `Prix (€)`,
            A.CodA as Agence,
            A.City_Address as `Ville agence`
        FROM BOOKING B
        JOIN TRAVEL_AGENCY A ON B.TRAVEL_AGENCY_CodA = A.CodA
        ORDER BY B.StartDate DESC
        LIMIT 10
    """)

    if not recent.empty:
        st.dataframe(recent, use_container_width=True)
    else:
        st.info("Aucune réservation récente")

except Exception as e:
    st.warning("Impossible de charger les réservations")

st.divider()
st.caption("📅 Module Réservations • Base: hotel")

st.dataframe(recent, use_container_width=True)


query = pd.read_sql_query(
    f"SELECT R.CodR, R.Floor, R.SurfaceArea, R.Type, MONTH(B.StartDate) AS month, B.Cost FROM ROOM R JOIN BOOKING B ON R.CodR = B.ROOM_CodR", con=engine)
res = query.groupby("month")["Cost"].sum().sort_values(ascending=False)
res.index = [calendar.month_name[i] for i in res.index]


st.dataframe(res, use_container_width=True)
st.divider()
st.line_chart(res)

booking_price = pd.read_sql_query(
    "SELECT * FROM BOOKING", con=engine).groupby("ROOM_CodR")['Cost'].sum()
st.dataframe(booking_price, use_container_width=True)
