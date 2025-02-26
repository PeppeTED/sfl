import streamlit as st
import pandas as pd
import plotly.express as px

# Caricare il file Excel
file_path = "sfl_2005.xlsx"  # Sostituisci con il tuo file
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

# Contare gli eventi per anno e classe
df_grouped = df.groupby([df["Snapshot Time"].dt.year, "Class"]).size().reset_index(name="Count")

# Creare il grafico interattivo con Plotly
fig = px.bar(df_grouped, x="Snapshot Time", y="Count", color="Class",
             title="Attività Solare nel Tempo",
             labels={"Snapshot Time": "Anno", "Count": "Numero di Eventi"},
             barmode="stack")

# Mostrare la dashboard
st.title("Dashboard Attività Solare")
st.plotly_chart(fig)

# Mostrare il dataframe con i dati filtrati
st.write("📊 **Dati elaborati:**")
st.dataframe(df)
