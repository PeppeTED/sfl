import streamlit as st
import pandas as pd
import plotly.express as px

# Caricare il file Excel
file_path = "sfl_2005.xlsx"  # File sfl dal 2005 pagina GOES archivio
df = pd.read_excel(file_path)

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

# Definire una palette di colori contrastanti per le classi
color_map = {
    'A': 'red',          # Rosso per A
    'B': 'orange',       # Arancio per B
    'C': 'yellow',       # Giallo per C
    'M': 'green',        # Verde per M
    'X': 'blue'          # Blu per X
}

# Contare gli eventi per anno e classe
df_grouped = df.groupby([df["Snapshot Time"].dt.year, "Class"]).size().reset_index(name="Count")

# Creare il grafico interattivo con Plotly
fig = px.bar(df_grouped, x="Snapshot Time", y="Count", color="Class",
             title="Attività Solare nel Tempo (Dati GOES)",
             labels={"Snapshot Time": "Anno", "Count": "Numero di Eventi"},
             barmode="stack", color_discrete_map=color_map)

# Aggiungere un layout personalizzato per migliorare la leggibilità
fig.update_layout(
    xaxis_title="Anno",
    yaxis_title="Numero di Eventi",
    legend_title="Classe",
    font=dict(
        family="Arial, sans-serif",
        size=12,
        color="Black"
    ),
    paper_bgcolor='white',
    plot_bgcolor='lightgray'
)

# Creare un menu laterale
st.sidebar.title("Menu")
menu = st.sidebar.radio("Seleziona una sezione:", ["Home", "Dati GOES"])

# Mostrare la sezione "Dati GOES"
if menu == "Dati GOES":
    st.title("Dati GOES: Attività Solare")
    st.plotly_chart(fig)
    st.write("📊 **Dati elaborati:**")
    st.dataframe(df)

# Altre sezioni possono essere aggiunte qui
if menu == "Home":
    st.title("Benvenuto nella Dashboard dell'Attività Solare")
    st.write("Seleziona la sezione 'Dati GOES' per visualizzare i grafici relativi all'attività solare.")
