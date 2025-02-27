import streamlit as st
import pandas as pd
import plotly.express as px

# Configurazione della pagina
st.set_page_config(page_title="Dashboard Attività Solare", layout="wide")

# Sidebar con menu navigabile
menu = st.sidebar.radio("Seleziona la visualizzazione", ["Attività Solare", "Analisi Avanzate"])

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

if menu == "Attività Solare":
    # Creare il grafico interattivo con colori
    fig = px.bar(
        df_grouped, x="Snapshot Time", y="Count", color="Class",
        title="Attività Solare nel Tempo",
        labels={"Snapshot Time": "Anno", "Count": "Numero di Eventi"},
        barmode="stack",
        color_discrete_map=color_map
    )

    # Mostrare la dashboard
    st.title("🌞 Dashboard Attività Solare")
    st.plotly_chart(fig, use_container_width=True)

    # Legenda personalizzata
    st.markdown("### 🔥 Intensità dei Solar Flare")
    for flare, color in color_map.items():
        st.markdown(f"🟢 **{flare}** - {color.capitalize()}")

    # Mostrare il dataframe con i dati filtrati
    st.write("📊 **Dati elaborati:**")
    st.dataframe(df)

elif menu == "Analisi Avanzate":
    st.title("📈 Analisi Avanzate")
    st.write("Qui potrai aggiungere ulteriori analisi, come il confronto con i dati del satellite Fermi.")
