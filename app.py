import streamlit as st
import numpy as np

from fetch_data import fetch_siirtymat_tyomarkkinoilla
from sankey import generate_sankey_figure


st.title("Siirtymät työmarkkinoilla")

df = fetch_siirtymat_tyomarkkinoilla()
df_to_display = df[0:3]

fig = generate_sankey_figure(df_to_display)

st.write(fig)

st.write(df_to_display)
