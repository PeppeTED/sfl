import streamlit as st
import pandas as pd
import plotly.express as px

# Caricare il file GOES
file_path_goes = "sfl_2005.xlsx"  # File sfl dal 2005 pagina GOES archivio
df_goes = pd.read_excel(file_path_goes)

# Pulire i nomi delle colonne
df_goes.columns = df_goes.columns.str.strip()

# Verificare se le colonne esistono nel file GOES
if "Snapshot Time" not in df_goes.columns or "Largest Event" not in df_goes.columns:
    st.error("Errore: Controlla i nomi delle colonne nel file GOES.")
    st.stop()

# Convertire la colonna in formato datetime per GOES
df_goes["Snapshot Time"] = pd.to_datetime(df_goes["Snapshot Time"], errors="coerce")

# Filtrare i dati dal 2005 per GOES
df_goes = df_goes[df_goes["Snapshot Time"].dt.year >= 2005]

# Estrarre la classe dell'evento solare per GOES
df_goes["Class"] = df_goes["Largest Event"].astype(str).str[0]

# Definire una palette di colori contrastanti per le classi di GOES
color_map_goes = {
    'A': 'red',          # Rosso per A
    'B': 'orange',       # Arancio per B
    'C': 'yellow',       # Giallo per C
    'M': 'green',        # Verde per M
    'X': 'blue'          # Blu per X
}

# Contare gli eventi per anno e classe per GOES
df_grouped_goes = df_goes.groupby([df_goes["Snapshot Time"].dt.year, "Class"]).size().reset_index(name="Count")

# Caricare il file FERMI
file_path_fermi = "GBM FERMI.xlsx"  # File dei dati FERMI
df_fermi = pd.read_excel(file_path_fermi)

# Pulire i nomi delle colonne del file FERMI
df_fermi.columns = df_fermi.columns.str.strip()

# Verificare se la colonna 'Date' esiste nel file FERMI
if "Date" not in df_fermi.columns:
    st.error("Errore: Controlla i nomi delle colonne nel file FERMI.")
    st.stop()

# Convertire la colonna 'Date' in formato datetime
df_fermi["Date"] = pd.to_datetime(df_fermi["Date"], errors="coerce")

# Filtrare i dati dal 2005 per FERMI
df_fermi = df_fermi[df_fermi["Date"].dt.year >= 2005]

# Contare il numero di eventi per anno nel file FERMI
df_grouped_fermi = df_fermi.groupby(df_fermi["Date"].dt.year).size().reset_index(name="Count")

# Creare un menu laterale con icone e un aspetto elegante
st.sidebar.title("Navigazione")
menu = st.sidebar.selectbox(
    "Seleziona una sezione:", 
    ["🏠 Home", "📊 Dati GOES", "📈 Dati FERMI", "🔍 Dettagli Eventi"]
)

# Sezione "Dati GOES"
if menu == "📊 Dati GOES":
    st.title("📊 Dati GOES: Attività Solare")
    st.plotly_chart(px.bar(df_grouped_goes, x="Snapshot Time", y="Count", color="Class",
                           title="Attività Solare nel Tempo (Dati GOES)",
                           labels={"Snapshot Time": "Anno", "Count": "Numero di Eventi"},
                           barmode="stack", color_discrete_map=color_map_goes))
    st.write("📊 **Dati elaborati (GOES):**")
    st.dataframe(df_goes)

# Sezione "Dati FERMI"
if menu == "📈 Dati FERMI":
    st.title("📈 Dati FERMI: Attività Solare")
    st.write("Grafico dei dati relativi agli eventi solari nel tempo (dal file FERMI).")
    # Creare il grafico a istogramma per i dati FERMI
    fig_fermi = px.bar(df_grouped_fermi, x="Date", y="Count",
                       title="Numero Totale di Eventi Solari (Dati FERMI)",
                       labels={"Date": "Anno", "Count": "Numero di Eventi"})
    st.plotly_chart(fig_fermi)
    st.write("📊 **Dati elaborati (FERMI):**")
    st.dataframe(df_fermi)

# Sezione "Home"
if menu == "🏠 Home":
    st.title("Benvenuto nella Dashboard dell'Attività Solare")
    st.write("Questa è la dashboard per visualizzare l'attività solare nel tempo.")
    st.write("Seleziona la sezione '📊 Dati GOES' per visualizzare il grafico relativo all'attività solare GOES, "
             "oppure '📈 Dati FERMI' per esplorare i dati FERMI.")

# Sezione "Dettagli Eventi"
if menu == "🔍 Dettagli Eventi":
    st.title("🔍 Dettagli Eventi Solari")
    st.write("In questa sezione, puoi approfondire i dettagli degli eventi solari registrati.")
    st.write("Clicca su '📊 Dati GOES' o '📈 Dati FERMI' per visualizzare i grafici e i dati relativi agli eventi solari.")
