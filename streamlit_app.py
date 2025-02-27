import streamlit as st
import pandas as pd
import plotly.express as px

# Configura la pagina
st.set_page_config(page_title="☀️ Attività Solare", page_icon="🌍", layout="wide")

# Titolo e descrizione
st.title("☀️ Dashboard Attività Solare")
st.markdown("📈 Visualizzazione dell'attività solare dal 2005 basata sui dati GOES.")

# Caricare il file Excel
file_path = "sfl_2005.xlsx"  # Assicurati che il file sia disponibile nel repository!
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    st.error("❌ Errore: Il file Excel non è stato trovato. Assicurati di caricarlo.")
    st.stop()

# Pulire i nomi delle colonne
df.columns = df.columns.str.strip()

# Verificare se le colonne esistono
if "Snapshot Time" not in df.columns or "Largest Event" not in df.columns:
    st.error("⚠️ Errore: Controlla i nomi delle colonne nel file Excel.")
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
fig = px.bar(
    df_grouped,
    x="Snapshot Time",
    y="Count",
    color="Class",
    title="🌟 Attività Solare dal 2005",
    labels={"Snapshot Time": "Anno", "Count": "Numero di Eventi"},
    barmode="stack",
    color_discrete_map={
        "A": "#636EFA",
        "B": "#EF553B",
        "C": "#00CC96",
        "M": "#AB63FA",
        "X": "#FFA15A"
    }
)

fig.update_layout(
    xaxis=dict(tickmode="linear"),
    hovermode="x unified",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

# Mostrare il grafico
st.plotly_chart(fig, use_container_width=True)

# Mostrare il dataframe con i dati filtrati
st.subheader("📊 Dati Elaborati")
st.dataframe(df.style.format({"Snapshot Time": lambda t: t.strftime("%Y-%m-%d") if pd.notnull(t) else ""}))

# Aggiungere un pulsante per scaricare i dati
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Scarica i dati", csv, "attivita_solare.csv", "text/csv", key="download-csv")

# Footer
st.markdown("---")
st.caption("🔬 Dati ottenuti dall'archivio GOES | Creato con ❤️ usando Streamlit & Plotly")
