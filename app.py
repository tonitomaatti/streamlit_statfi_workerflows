import streamlit as st
import numpy as np
import plotly

from fetch_data import fetch_siirtymat_tyomarkkinoilla
from sankey import generate_sankey_figure

st.set_page_config(layout="wide")

st.title("Työvoimavirrat 2007Q4 - 2019Q3")
st.text("Siirtymät työmarkkinoilla edellisestä vuosineljänneksestä, 15-74 -vuotiaat")

df = fetch_siirtymat_tyomarkkinoilla()

quarters = list(df.index.values)

# Aloitetaan df yksi eteenpäin: Siirtymät työmarkkinoilla edellisestä vuosineljänneksestä,

start, end = st.select_slider(
    label="",
    options=[i for i in range(0, len(quarters))],  # quarters,
    value=(0, 9),
    format_func=lambda x: quarters[x],
)

col1, col2 = st.columns([5, 1])

df_start = start if start == end else start + 1

df_to_display = df.iloc[df_start : end + 1]
fig = generate_sankey_figure(
    df_to_display, list(df.iloc[df_start - 1 : end + 1].index.values)
)

# print(fig.__dict__)
# st.write(range_slider)

col1.plotly_chart(fig, use_container_width=True)

## Metrics
# Calculate start and end
tyolliset_start = (
    df_to_display.iloc[0, 0] + df_to_display.iloc[0, 1] + df_to_display.iloc[0, 2]
)
tyottomat_start = (
    df_to_display.iloc[0, 3] + df_to_display.iloc[0, 4] + df_to_display.iloc[0, 5]
)
tyov_ulkop_start = (
    df_to_display.iloc[0, 6] + df_to_display.iloc[0, 7] + df_to_display.iloc[0, 8]
)

tyolliset_end = (
    df_to_display.iloc[-1, 0] + df_to_display.iloc[-1, 3] + df_to_display.iloc[-1, 6]
)
tyottomat_end = (
    df_to_display.iloc[-1, 1] + df_to_display.iloc[-1, 4] + df_to_display.iloc[-1, 7]
)
tyov_ulkop_end = (
    df_to_display.iloc[-1, 2] + df_to_display.iloc[-1, 5] + df_to_display.iloc[-1, 8]
)

tyolliset_change = tyolliset_end - tyolliset_start
tyottomat_change = tyottomat_end - tyottomat_start
tyov_ulkop_change = tyov_ulkop_end - tyov_ulkop_start

col2.markdown("**Virtojen\nloppumäärät\n(1000 henkilöä)**")
col2.metric(label="Työlliset", value=str(tyolliset_end), delta=str(tyolliset_change))
col2.metric(
    label="Työvoiman ulkopuolella",
    value=str(tyov_ulkop_end),
    delta=str(tyov_ulkop_change),
    delta_color="off",
)
col2.metric(
    label="Työttömät",
    value=str(tyottomat_end),
    delta=str(tyottomat_change),
    delta_color="inverse",
)

# st.write(df_to_display)
