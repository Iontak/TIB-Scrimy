import streamlit as st
import pandas as pd

st.set_page_config(page_title="TIB Scrimy Rozdělovací Appka", layout="wide")

# Načtení dat
hraci_data = pd.read_excel("TIB_Scrimy.xlsx", engine="openpyxl")

# Ověření existence sloupce 'hrac'
if "hrac" not in hraci_data.columns:
    st.error("Excelový soubor musí obsahovat sloupec s názvem 'hrac'")
    st.stop()

# Výběr přítomných hráčů – postranní panel
st.sidebar.header("Dnešní přítomnost hráčů")
vsichni_hraci = hraci_data["hrac"].tolist()
pritomni_hraci = st.sidebar.multiselect("Vyber hráče, kteří jsou dnes přítomni:", vsichni_hraci, default=vsichni_hraci)

# Filtrování na základě přítomnosti
pritomni_df = hraci_data[hraci_data["hrac"].isin(pritomni_hraci)]

# Inicializace session state pro týmy
if "team1" not in st.session_state:
    st.session_state.team1 = []

if "team2" not in st.session_state:
    st.session_state.team2 = []

st.title("🏆 TIB Scrimy Rozdělovací Appka")

col1, col2 = st.columns(2)

# Výběr hráčů do týmů
with col1:
    st.subheader("Tým 1")
    dostupni_pro_team1 = [hrac for hrac in pritomni_df["hrac"] if hrac not in st.session_state.team1 and hrac not in st.session_state.team2]
    vyber_hrace1 = st.selectbox("Přidej hráče do Týmu 1", [""] + dostupni_pro_team1, key="vyber1")
    if vyber_hrace1 and st.button("➕ Přidat do Týmu 1"):
        st.session_state.team1.append(vyber_hrace1)

with col2:
    st.subheader("Tým 2")
    dostupni_pro_team2 = [hrac for hrac in pritomni_df["hrac"] if hrac not in st.session_state.team2 and hrac not in st.session_state.team1]
    vyber_hrace2 = st.selectbox("Přidej hráče do Týmu 2", [""] + dostupni_pro_team2, key="vyber2")
    if vyber_hrace2 and st.button("➕ Přidat do Týmu 2"):
        st.session_state.team2.append(vyber_hrace2)

# Zobrazení týmů
col3, col4 = st.columns(2)

with col3:
    st.subheader("👥 Složení Týmu 1")
    st.write(st.session_state.team1)

with col4:
    st.subheader("👥 Složení Týmu 2")
    st.write(st.session_state.team2)

# Tabulka zbývajících hráčů
zbyvajici_hraci = [hrac for hrac in pritomni_hraci if hrac not in st.session_state.team1 and hrac not in st.session_state.team2]
st.subheader("📝 Dostupní hráči k rozřazení")
st.table(pritomni_df[pritomni_df["hrac"].isin(zbyvajici_hraci)])

# Reset tlačítko
if st.button("🔄 Resetovat týmy"):
    st.session_state.team1 = []
    st.session_state.team2 = []
