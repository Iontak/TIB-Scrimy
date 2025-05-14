import streamlit as st
import pandas as pd

# Načtení dat ze souboru
hraci_data = pd.read_excel("TIB_Scrimy.xlsx", engine="openpyxl")

# Očištění názvů sloupců
hraci_data.columns = hraci_data.columns.str.strip()

# Výpis sloupců pro ladění (můžeš případně odstranit)
st.write("Sloupce v Excelu:", hraci_data.columns.tolist())

# Inicializace stavových proměnných
if "team1" not in st.session_state:
    st.session_state.team1 = []

if "team2" not in st.session_state:
    st.session_state.team2 = []

if "ulozene_tymy" not in st.session_state:
    st.session_state.ulozene_tymy = []

st.title("TIB Scrimy týmy")

# Výběr hráčů pro tým 1 a tým 2 vedle sebe
col1, col2 = st.columns(2)

with col1:
    st.subheader("Tým 1")
    vyber1 = st.multiselect(
        "Vyber až 5 hráčů pro tým 1:",
        options=[hrac for hrac in hraci_data["Hrac"] if hrac not in st.session_state.team2],
        default=st.session_state.team1,
        key="vyber1"
    )

with col2:
    st.subheader("Tým 2")
    vyber2 = st.multiselect(
        "Vyber až 5 hráčů pro tým 2:",
        options=[hrac for hrac in hraci_data["Hrac"] if hrac not in st.session_state.team1],
        default=st.session_state.team2,
        key="vyber2"
    )

# Funkce pro výpis týmu
def zobrazit_tym(jmeno, vyber):
    df_vyber = hraci_data[hraci_data["Hrac"].isin(vyber)]
    soucet = df_vyber["Body"].sum()
    st.subheader(f"{jmeno} ( {soucet} bodů)")
    st.dataframe(df_vyber)

# Zobraz oba týmy
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    zobrazit_tym("Tým 1", vyber1)
with col2:
    zobrazit_tym("Tým 2", vyber2)

# Uložení týmů
if st.button("💾 Uložit kombinaci"):
    if len(vyber1) == 5 and len(vyber2) == 5:
        st.session_state.ulozene_tymy.append({
            "team1": vyber1.copy(),
            "team2": vyber2.copy()
        })
        st.success("Týmy byly uloženy!")
    else:
        st.warning("Musíš vybrat přesně 5 hráčů do každého týmu!")

# Zobrazení uložených týmů
if st.session_state.ulozene_tymy:
    st.markdown("---")
    st.subheader("📁 Uložené kombinace")
    for i, kombinace in enumerate(st.session_state.ulozene_tymy, 1):
        st.markdown(f"**{i}.** 🟥 {', '.join(kombinace['team1'])} vs 🟦 {', '.join(kombinace['team2'])}")

# Tabulka všech hráčů s informací o jejich zařazení
st.markdown("---")
st.subheader(" Přehled hráčů")

# Vytvoříme nový DataFrame s příznakem "Tým"
prehled_hracu = hraci_data.copy()
prehled_hracu["Tým"] = prehled_hracu["Hrac"].apply(lambda x:
    "Tým 1" if x in vyber1 else ("Tým 2" if x in vyber2 else "Volný"))

# Seřadíme: nejdřív Tým 1, pak Tým 2, pak Volní
poradi = {"Tým 1": 0, "Tým 2": 1, "Volný": 2}
prehled_hracu["Pořadí"] = prehled_hracu["Tým"].map(poradi)
prehled_hracu = prehled_hracu.sort_values("Pořadí").drop(columns=["Pořadí"])

# Zobrazíme přehled
st.dataframe(prehled_hracu, use_container_width=True)

# Reset aplikace
if st.button("🔄 Resetovat výběr"):
    st.session_state.team1 = []
    st.session_state.team2 = []
    st.session_state.ulozene_tymy = []
    st.experimental_rerun()
