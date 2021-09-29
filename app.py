import streamlit as st
import numpy as np
import plotly

from fetch_data import fetch_siirtymat_tyomarkkinoilla
from sankey import generate_sankey_figure

st.set_page_config(layout="wide")

st.title("Siirtymät työmarkkinoilla")

df = fetch_siirtymat_tyomarkkinoilla()

quarters = list(df.index.values)

# Aloitetaan df yksi eteenpäin: Siirtymät työmarkkinoilla edellisestä vuosineljänneksestä,

with st.container():

    start, end = st.select_slider(
        label="",
        options=[i for i in range(0, len(quarters))],  # quarters,
        value=(0, 9),
        format_func=lambda x: quarters[x],
    )

    df_start = start if start == end else start + 1

    df_to_display = df.iloc[df_start : end + 1]
    fig = generate_sankey_figure(df_to_display)
    st.plotly_chart(fig, use_container_width=True)
    st.write(df_to_display)

# st.write(df_to_display)
