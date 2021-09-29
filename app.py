import streamlit as st
import numpy as np

from fetch_data import fetch_siirtymat_tyomarkkinoilla


st.title('Siirtymät työmarkkinoilla')

df = fetch_siirtymat_tyomarkkinoilla()
st.write(df)