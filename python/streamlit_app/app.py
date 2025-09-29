import pandas as pd
import streamlit as st

st.set_page_config(page_title="Vibe Demo – Streamlit", layout="wide")
st.title("Vibe Demo – Streamlit")

st.markdown("KPI’er på tværs af niveauer (global/EU/Norden/DK) – data indsættes senere.")
df = pd.DataFrame({"level": ["Global","EU","Nordic","DK"], "value":[None,None,None,None]})
st.dataframe(df, use_container_width=True)
