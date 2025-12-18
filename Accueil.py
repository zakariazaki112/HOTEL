#texte
import streamlit as st
import pandas as pd


# ================== CONFIG ==================
st.set_page_config(
    page_title="Hôtel Management System",
    page_icon="🏨",
    layout="wide"
)

# ================== STYLE PREMIUM ==================
st.markdown("""
<style>

/* ----- BACKGROUND ----- */
body {
    background: linear-gradient(180deg, #F1F8E9, #FFFFFF);
}

/* ----- TITRES ----- */
h1, h2, h3 {
    color: white;
    font-weight: 800;
}

.hero-title {
    font-size: 52px;
    font-weight: 900;
    color: white;
}

.hero-subtitle {
    font-size: 22px;
    color: white;
}

/* ----- METRICS ----- */
div[data-testid="metric-container"] {
    background: white;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

div[data-testid="metric-container"]:hover {
    transform: scale(1.05);
}

/* ----- CARDS ----- */
.card {
    background: rgba(41, 44, 50, 0.5);
    padding: 30px;
    border-radius: 22px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.1);
    text-align: center;
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

/* ----- BUTTONS ----- */
button {
    border-bottom: rgba(252, 35, 37, 1) !important;
    color: white !important;
    font-weight: 700 !important;
}

/* ----- SIDEBAR ----- */
section[data-testid="stSidebar"] {
    background: #0e1117;
}

/* ----- FOOTER ----- */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ================== HERO SECTION ==================
st.markdown("<div class='hero-title'>🏨 Hôtel Management System</div>", unsafe_allow_html=True)
st.markdown("<div class='hero-subtitle'>Plateforme intelligente de gestion hôtelière</div>", unsafe_allow_html=True)
st.markdown("### ✨ Gérez vos agences, chambres et réservations en toute simplicité")
st.divider()

# ================== METRICS ==================
col1, col2, col3 = st.columns(3)

try:
    nb_agences = pd.read_sql_query("SELECT COUNT(*) total FROM TRAVEL_AGENCY").iloc[0, 0]
    nb_chambres = pd.read_sql_query("SELECT COUNT(*) total FROM ROOM").iloc[0, 0]
    nb_reservations = pd.read_sql_query("SELECT COUNT(*) total FROM BOOKING").iloc[0, 0]
except:
    nb_agences = nb_chambres = nb_reservations = 0

col1.metric("📍 Agences partenaires", nb_agences)
col2.metric("🛏️ Chambres disponibles", nb_chambres)
col3.metric("📅 Réservations totales", nb_reservations)

st.divider()

# ================== GALERIE IMMERSIVE ==================
st.subheader("🖼️ Expérience & Confort")

tabs = st.tabs(["🛏️ Chambre Simple", "👫 Chambre Double", "👑 Suite de Luxe"])

with tabs[0]:
    st.image("https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=1200",
        
        caption="Chambre simple – confort et élégance"
        ,
        use_column_width=True
    )

with tabs[1]:
    st.image(
        "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=1200",
        
        caption="Chambre double – idéale pour les couples",
        use_column_width=True
    )

with tabs[2]:
    st.image(
        "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=1200",
        
        caption="Suite de luxe – espace et raffinement"
        ,
        use_column_width=True
    )

st.divider()

# ================== SERVICES ==================
st.subheader("🌟 Fonctionnalités Principales")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class='card'>
        📍<br><br>
        <b>Gestion des Agences</b><br><br>
        Visualisation géographique, statistiques et recherche par ville.
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='card'>
        🛏️<br><br>
        <b>Gestion des Chambres</b><br><br>
        Filtres par type, équipements et affichage interactif.
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='card'>
        📊<br><br>
        <b>Analyse des Réservations</b><br><br>
        Évolution des prix et tendances mensuelles.
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ================== À PROPOS ==================
st.subheader("💼 À propos du projet")

st.info("""
🎯 **Objectif**

Concevoir une application web moderne permettant la gestion complète
des réservations d'une chaîne hôtelière à l'aide de Streamlit et MySQL.
""")

st.success("""
👩‍🎓 **Réalisé par**

**Sophia Yassfouli**

**Badr Eddaoudi**

**Marwa Aqrir**

**Zakaria Zaki**

**Ayoub Sabri**

**Asma Bennani**

ENSA  
Python • Streamlit • MySQL • SQLAlchemy
""")

# ================== SIDEBAR ==================
with st.sidebar:
    st.header("🧭 Navigation")
    st.write("""
- 🏠 Accueil  
- 📍 Agences  
- 🛏️ Chambres  
- 📅 Réservations  
""")

    st.divider()
    st.caption("🏨 Hôtel Management System • 2024")