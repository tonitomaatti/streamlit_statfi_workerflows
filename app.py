import streamlit as st
import numpy as np
import plotly

from fetch_data import fetch_siirtymat_tyomarkkinoilla
from sankey import generate_sankey_figure

st.set_page_config(layout="wide")

st.title("Siirtymät työmarkkinoilla")

df = fetch_siirtymat_tyomarkkinoilla()

quarters = list(df.index.values)

with st.container():

    start, end = st.select_slider(
        label="",
        options=quarters,
        value=(quarters[0], quarters[9]),
    )
    df_to_display = df[start:end]
    fig = generate_sankey_figure(df_to_display)
    st.plotly_chart(fig, use_container_width=True)

st.write(df_to_display)
