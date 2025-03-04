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
    df_goes_grouped = df_goes.groupby([df_goes["Snapshot Time"].dt.date, "Class"]).size().reset_index(name="Count")

    # Grafico GOES
    fig_goes = px.bar(
        df_goes_grouped, x="Snapshot Time", y="Count", color="Class",
        title="Attività Solare GOES",
        labels={"Snapshot Time": "Data", "Count": "Numero di Eventi"},
        barmode="stack",
        color_discrete_map=color_map
    )

    st.plotly_chart(fig_goes, use_container_width=True)

    # Sezione: Analisi Avanzate
elif selected == "🚀 Analisi Avanzate":
    st.title("📈 Analisi Avanzate")

    # Creare un dataset combinato per confrontare i dati di Fermi e GOES
    df_fermi_grouped = df_fermi.groupby([df_fermi["Date"].dt.date, "Time"]).size().reset_index(name="Count_Fermi")
    df_goes_grouped["Snapshot Time"] = pd.to_datetime(df_goes_grouped["Snapshot Time"])

    # Unire i due dataframe (Fermi e GOES)
    df_combined = pd.merge(df_goes_grouped, df_fermi_grouped, left_on=["Snapshot Time", "Class"], right_on=["Date", "Time"], how="outer")

    # Grafico di confronto tra GOES e Fermi
    fig_comparison = px.bar(
        df_combined, x="Snapshot Time", y=["Count", "Count_Fermi"],
        title="Confronto Attività Solare: GOES vs Fermi",
        labels={"Snapshot Time": "Data", "value": "Numero di Eventi"},
        barmode="group"
    )

    st.plotly_chart(fig_comparison, use_container_width=True)

    # Mostrare il dataframe combinato
    st.write("📊 **Confronto Dati GOES vs Fermi:**")
    st.dataframe(df_combined)
