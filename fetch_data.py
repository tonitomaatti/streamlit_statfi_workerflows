import requests
import pandas as pd
from io import StringIO
import streamlit as st


@st.cache(suppress_st_warning=True)
def fetch_siirtymat_tyomarkkinoilla():
    body = {
        "query": [
            {"code": "Sukupuoli", "selection": {"filter": "item", "values": ["SSS"]}},
            {
                "code": "Tiedot",
                "selection": {
                    "filter": "item",
                    "values": [
                        "v1_to_1",
                        "v1_to_2",
                        "v1_to_4",
                        "v2_to_1",
                        "v2_to_2",
                        "v2_to_4",
                        "v4_to_1",
                        "v4_to_2",
                        "v4_to_4",
                        "vJ_to_J",
                    ],
                },
            },
        ],
        "response": {"format": "csv"},
    }

    r = requests.post(
        "https://pxnet2.stat.fi:443/PXWeb/api/v1/fi/Kokeelliset_tilastot/tyvir/koeti_tyvir_pxt_12aj.px",
        json=body,
    )
    print(r)

    df = pd.read_csv(StringIO(r.text), sep=",", index_col="Vuosineljännes")
    df = df.drop(columns=["Sukupuoli"])

    return df
