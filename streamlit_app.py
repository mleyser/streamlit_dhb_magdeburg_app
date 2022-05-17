import streamlit as st
import snowflake.connector
import pandas as pd
from PIL import Image

st.set_page_config(page_title = "SC Magdeburg", layout = "wide")

# Check and printing sf connections
st.text("Establishing Snowflake connection...")
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
st.text("User | Account | Region")
my_cur.execute("SELECT CURRENT_USER, CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
st.text(my_data_row)

st.markdown("---")


# actual team info
st.title('SC Magdeburg | Saison 2021/22')

image = Image.open('kader_magdeburg.jpg')
st.image(image)

st.markdown("---")

st.header("Teamstatistik")

col1, col2 = st.columns(2)

#col1.subheader('Platzierungen Saison 2021/22')
col1.markdown('**Tabellenplatz**: 1️⃣')
col1.markdown('**Siege** | **Unentschieden** | **Niederlagen** : 27 | 0 | 2')
col1.markdown('**Tore**: 893')
col1.markdown("**Gegentore**: 751")
col1.markdown("**Differenz**: 142")
col1.markdown("**Bester 7m-Schütze**: Omar Ingi Magnusson(90/121/91.5%)")
col1.markdown("**Sünder**: Piotr Chrapkowski(51)")
col1.markdown("**Ticketverkäufe**: 107477")


tabellenstand = Image.open('tabelle_hist_magdeburg.png')
col2.image(tabellenstand)

st.markdown("---")

st.header("Spieler Gesamtstatistik")


#st.text("Spaltennamen | 0️⃣: Nachname, 1️⃣: Vorname, 2️⃣: POS, 3️⃣: S, 4️⃣: T, 5️⃣: FW, 6️⃣: FT, 7️⃣: 7M")
#st.text("8️⃣: %, 9️⃣: AS, 1️⃣0️⃣: TF, 1️⃣1️⃣: ST, 1️⃣2️⃣: BL, 1️⃣3️⃣: GK, 1️⃣4️⃣: 2M, 1️⃣5️⃣: RK, 1️⃣6️⃣: BK")
#my_cur.execute("SELECT * FROM kader_magdeburg")
#my_data_rows = my_cur.fetchall()
#data_berlin = st.dataframe(my_data_rows)

@st.cache
def get_data_from_csv():
  df = pd.read_csv("kader_magdeburg_index_false.csv")
  return df
df = get_data_from_csv()
  
rad = st.sidebar.radio("Navigation",["Gesamtansicht","Gefilterte Ansicht"])

# Sidebar
with st.sidebar.container():
  logo = Image.open('dhb_logo.png')
  st.image(logo, use_column_width=True)


if rad == "Gesamtansicht":
  st.text("Erstansicht absteigend nach geworfenen Toren sortiert")
  st.dataframe(df)

if rad == "Gefilterte Ansicht":
  st.text("Erstansicht zeigt Stammtorhüter")
  st.sidebar.header("Hier Filter wählen:")

  positionen = st.sidebar.multiselect("Spielposition (Angriffsmodus):", options = df["Position"].unique(), default = df["Position"].unique())

  nachname = st.sidebar.multiselect("Spieler (Nachname):",options = df["Nachname"].unique(), default = ["Green"])

  df_selection = df.query("Position == @positionen & Nachname == @nachname")

  st.dataframe(df_selection)
