import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurazione della pagina
st.set_page_config(page_title="Dashboard Attività Solare", layout="wide")

# MENU NAVIGABILE ORIZZONTALE
selected = option_menu(
    menu_title=None,  
    options=["📊 Attività Solare", "🚀 Analisi Avanzate"],  
    icons=["bar-chart", "line-chart"],  
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "20px"},
        "nav-link": {"font-size": "18px", "text-align": "center", "margin": "0px"},
        "nav-link-selected": {"background-color": "#FF5733"},
    }
)

# Caricare il file GOES
file_path_goes = "sfl_2005.xlsx"  # Modifica con il tuo file GOES
try:
    df_goes = pd.read_excel(file_path_goes)
except FileNotFoundError:
    st.error("Errore: File GOES non trovato.")
    st.stop()

# Pulire i nomi delle colonne
df_goes.columns = df_goes.columns.str.strip()

# Verificare se le colonne esistono
if "Snapshot Time" not in df_goes.columns or "Largest Event" not in df_goes.columns:
    st.error("Errore: Controlla i nomi delle colonne nel file GOES.")
    st.stop()

# Caricare il file Fermi
file_path_fermi = "GBM FERMI.xlsx"  # Modifica con il tuo file Fermi
try:
    df_fermi = pd.read_excel(file_path_fermi)
except FileNotFoundError:
    st.error("Errore: File Fermi non trovato.")
    st.stop()

# Pulire i nomi delle colonne
df_fermi.columns = df_fermi.columns.str.strip()

# Verifica che esista una colonna di tempo e data
if "Date" not in df_fermi.columns or "Time" not in df_fermi.columns:
    st.error("Errore: Controlla i nomi delle colonne nel file Fermi.")
    st.stop()

# Convertire la colonna in formato datetime (per entrambi i file)
df_goes["Snapshot Time"] = pd.to_datetime(df_goes["Snapshot Time"], errors="coerce")
df_fermi["Date"] = pd.to_datetime(df_fermi["Date"], errors="coerce")

# Sezione: Attività Solare GOES
if selected == "📊 Attività Solare":
    st.title("🌞 Attività Solare nel Tempo")

    # Elenco dei flares per GOES
    df_goes["Class"] = df_goes["Largest Event"].astype(str).str[0]
    color_map = {"A": "blue", "B": "cyan", "C": "green", "M": "orange", "X": "red"}

    # Raggruppamento annuale dei dati GOES
    df_goes["Year"] = df_goes["Snapshot Time"].dt.year
    df_goes_grouped = df_goes.groupby([df_goes["Year"], "Class"]).size().reset_index(name="Count")

    # Grafico GOES - Istogramma annuale
    fig_goes = px.histogram(
        df_goes_grouped, x="Year", y="Count", color="Class",
        title="Attività Solare GOES (Istogramma Annuale)",
        labels={"Year": "Anno", "Count": "Numero di Eventi"},
        histfunc="sum",
        color_discrete_map=color_map
    )

    # Dividere la pagina in 2 colonne
    col1, col2 = st.columns(2)

    # Mostrare il grafico GOES nella prima colonna
    with col1:
        st.plotly_chart(fig_goes, use_container_width=True)

    # Creare il dataframe per il confronto con Fermi
    df_fermi["Year"] = df_fermi["Date"].dt.year
    df_fermi_grouped = df_fermi.groupby([df_fermi["Year"], "Time"]).size().reset_index(name="Count_Fermi")

    # Unire i due dataframe (Fermi e GOES)
    df_combined = pd.merge(df_goes_grouped, df_fermi_grouped, left_on="Year", right_on="Year", how="outer")

    # Grafico di confronto tra GOES e Fermi - Istogramma annuale
    fig_comparison = px.histogram(
        df_combined, x="Year", y=["Count", "Count_Fermi"],
        title="Confronto Attività Solare: GOES vs Fermi (Istogramma Annuale)",
        labels={"Year": "Anno", "value": "Numero di Eventi"},
        histfunc="sum",
        barmode="group"
    )

    # Mostrare il grafico di confronto nella seconda colonna
    with col2:
        st.plotly_chart(fig_comparison, use_container_width=True)
