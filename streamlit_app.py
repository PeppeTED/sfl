import streamlit as st
import pandas as pd
import plotly.express as px

# Impostare la configurazione della pagina
st.set_page_config(page_title="Dashboard Attività Solare", layout="wide")

# Sidebar con il menu di navigazione
st.sidebar.title("🌞 Menu di Navigazione")
menu_option = st.sidebar.radio("Seleziona una sezione:", ["Home", "Dati GOES", "Dati FERMI"])

# Sezione Home
if menu_option == "Home":
    st.title("🌟 Dashboard sull'Attività Solare")
    st.subheader("Benvenuto nella Dashboard Interattiva!")
    st.markdown(
        """
        Questa dashboard ti permette di esplorare l'attività solare nel tempo attraverso dati provenienti da diverse missioni spaziali.
        
        - **Dati GOES**: Analizza gli eventi solari più significativi registrati dai satelliti GOES dal 2005.
        - **Dati FERMI**: Visualizza il numero totale di eventi solari rilevati dal satellite FERMI.
        
        📈 Utilizza il menu laterale per navigare tra le sezioni e scoprire le analisi!
        """
    )
    
    # Aggiungere un'immagine decorativa
    st.image("https://upload.wikimedia.org/wikipedia/commons/3/3a/Solar_flare_CME.jpg", caption="Eruzione solare", use_column_width=True)
    
    st.markdown("---")
    st.info("🔍 Questa dashboard è stata creata per analizzare e visualizzare l'attività del Sole utilizzando dati storici.")

# Sezione Dati GOES
elif menu_option == "Dati GOES":
    st.title("📊 Analisi Dati GOES")
    
    # Caricare il file GOES
    file_path_goes = "sfl_2005.xlsx"  # File dei dati GOES
    df_goes = pd.read_excel(file_path_goes)
    df_goes.columns = df_goes.columns.str.strip()
    
    if "Snapshot Time" not in df_goes.columns or "Largest Event" not in df_goes.columns:
        st.error("Errore: Controlla i nomi delle colonne nel file GOES.")
        st.stop()
    
    df_goes["Snapshot Time"] = pd.to_datetime(df_goes["Snapshot Time"], errors="coerce")
    df_goes = df_goes[df_goes["Snapshot Time"].dt.year >= 2005]
    df_goes["Class"] = df_goes["Largest Event"].astype(str).str[0]
    
    # Mappare colori per la potenza delle classi
    color_map = {"A": "blue", "B": "green", "C": "yellow", "M": "orange", "X": "red"}
    df_grouped_goes = df_goes.groupby([df_goes["Snapshot Time"].dt.year, "Class"]).size().reset_index(name="Count")
    
    fig_goes = px.bar(df_grouped_goes, x="Snapshot Time", y="Count", color="Class", 
                      title="Attività Solare nel Tempo (GOES)",
                      labels={"Snapshot Time": "Anno", "Count": "Numero di Eventi"},
                      barmode="stack", color_discrete_map=color_map)
    
    st.plotly_chart(fig_goes)
    st.write("📊 **Dati elaborati (GOES):**")
    st.dataframe(df_goes)

# Sezione Dati FERMI
elif menu_option == "Dati FERMI":
    st.title("📈 Analisi Dati FERMI")
    
    # Caricare il file FERMI
    file_path_fermi = "GBM FERMI.xlsx"
    df_fermi = pd.read_excel(file_path_fermi)
    df_fermi.columns = df_fermi.columns.str.strip()
    
    if "Date" not in df_fermi.columns:
        st.error("Errore: Controlla i nomi delle colonne nel file FERMI.")
        st.stop()
    
    df_fermi["Date"] = pd.to_datetime(df_fermi["Date"], errors="coerce")
    df_fermi = df_fermi[df_fermi["Date"].dt.year >= 2005]
    
    df_grouped_fermi = df_fermi.groupby(df_fermi["Date"].dt.year).size().reset_index(name="Count")
    
    fig_fermi = px.bar(df_grouped_fermi, x="Date", y="Count", 
                       title="Numero Totale di Eventi Solari (Dati FERMI)",
                       labels={"Date": "Anno", "Count": "Numero di Eventi"})
    
    st.plotly_chart(fig_fermi)
    st.write("📊 **Dati elaborati (FERMI):**")
    st.dataframe(df_fermi)
