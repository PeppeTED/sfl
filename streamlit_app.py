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

# Caricare il file Excel
file_path = "sfl_2005.xlsx"  # Modifica con il tuo file
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error("Errore: File non trovato. Assicurati di aver caricato il file corretto.")
    st.stop()

# Pulire i nomi delle colonne
df.columns = df.columns.str.strip()

# Verificare se le colonne esistono
if "Snapshot Time" not in df.columns or "Largest Event" not in df.columns:
    st.error("Errore: Controlla i nomi delle colonne nel file Excel.")
    st.stop()

# Convertire la colonna in formato datetime
df["Snapshot Time"] = pd.to_datetime(df["Snapshot Time"], errors="coerce")

# Filtrare i dati dal 2005
df = df[df["Snapshot Time"].dt.year >= 2005]

# Estrarre la classe dell'evento solare
df["Class"] = df["Largest Event"].astype(str).str[0]

# Mappare i colori in base all'intensità dei flare
color_map = {"A": "blue", "B": "cyan", "C": "green", "M": "orange", "X": "red"}

# Contare gli eventi per anno e classe
df_grouped = df.groupby([df["Snapshot Time"].dt.year, "Class"]).size().reset_index(name="Count")

# Sezione: ATTIVITÀ SOLARE
if selected == "📊 Attività Solare":
    st.title("🌞 Attività Solare nel Tempo")

    # Creare il grafico interattivo con colori
    fig = px.bar(
        df_grouped, x="Snapshot Time", y="Count", color="Class",
        title="Attività Solare nel Tempo",
        labels={"Snapshot Time": "Anno", "Count": "Numero di Eventi"},
        barmode="stack",
        color_discrete_map=color_map
    )

    st.plotly_chart(fig, use_container_width=True)

    # Legenda personalizzata
    st.markdown("### 🔥 Intensità dei Solar Flare")
    legenda = {
        "A": "🔵 Debole",
        "B": "🔹 Basso",
        "C": "🟢 Moderato",
        "M": "🟠 Forte",
        "X": "🔴 Estremo"
    }
    for flare, desc in legenda.items():
        st.markdown(f"**{flare}** - {desc}")

    # Mostrare il dataframe con i dati filtrati
    st.write("📊 **Dati elaborati:**")
    st.dataframe(df)

# Sezione: ANALISI AVANZATE
elif selected == "🚀 Analisi Avanzate":
    st.title("📈 Analisi Avanzate")
    st.write("Qui potrai aggiungere ulteriori analisi, come il confronto con i dati del satellite Fermi.")
