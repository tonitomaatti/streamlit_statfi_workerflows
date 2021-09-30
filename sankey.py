import plotly.graph_objects as go
import streamlit as st
import numpy as np


@st.cache(suppress_st_warning=True)
def generate_sankey_data(df):
    # Lasketaan nodejen alkupaikat
    rows_n = (
        len(df) + 1
    )  # Rivien määrä. Lasketaan offset. +1 koska alussa "haamurivi" ekalle lähteelle
    tyottomat_offset = rows_n
    tyov_ulkop_offset = tyottomat_offset + rows_n

    # Color palette:
    green = "rgba(0,132,80, 0.4)"
    red = "rgba(184,29,19, 0.4)"
    yellow = "rgba(239,183,0, 0.4)"

    # Labelit, värit ja paikat nodeille
    labels = ["Työlliset"] + [None for i in range(1, rows_n)]
    node_colors = [green for i in range(0, rows_n)]
    node_x = list(np.linspace(0, 1, rows_n, endpoint=True))
    node_y = [0 for i in range(0, rows_n)]

    labels = labels + ["Työttömät"] + [None for i in range(1, rows_n)]
    node_colors = node_colors + [red for i in range(0, rows_n)]
    node_x = node_x + list(np.linspace(0, 1, rows_n, endpoint=True))
    node_y = node_y + [0.5 for i in range(0, rows_n)]

    labels = labels + ["Työvoiman ulkopuolella"] + [None for i in range(1, rows_n)]
    node_colors = node_colors + [yellow for i in range(0, rows_n)]
    node_x = node_x + list(np.linspace(0, 1, rows_n, endpoint=True))
    node_y = node_y + [0.9 for i in range(0, rows_n)]

    # Värit nodeille
    # node_color_map = {
    #    "Työlliset": green,
    #    "Työttömät": red,
    #    "Työvoiman ulkopuolella": yellow,
    # }
    # node_colors = [node_color_map[node_type] for node_type in labels]

    source = []
    target = []
    value = []
    link_colors = []

    for i in range(0, len(df)):

        # Tyollisenä pysyneet
        source.append(i)
        target.append(i + 1)
        value.append(df.iloc[i, 0])
        link_colors.append(green)

        # Työllisestä työttömäksi
        source.append(i)
        target.append(tyottomat_offset + i + 1)
        value.append(df.iloc[i, 1])
        link_colors.append(green)

        # Työttömästä työlliseksi
        source.append(tyottomat_offset + i)
        target.append(i + 1)
        value.append(df.iloc[i, 3])
        link_colors.append(red)

        # Työttömänä pysyneet
        source.append(tyottomat_offset + i)
        target.append(tyottomat_offset + i + 1)
        value.append(df.iloc[i, 4])
        link_colors.append(red)

        # Työllisestä työvoiman ulkopuolelle
        source.append(i)
        target.append(tyov_ulkop_offset + i + 1)
        value.append(df.iloc[i, 2])
        link_colors.append(green)

        # Työttömästä työvoiman ulkopuolelle
        source.append(tyottomat_offset + i)
        target.append(tyov_ulkop_offset + i + 1)
        value.append(df.iloc[i, 5])
        link_colors.append(red)

        # Työvoiman ulkopuolella pysyneet
        source.append(tyov_ulkop_offset + i)
        target.append(tyov_ulkop_offset + i + 1)
        value.append(df.iloc[i, 8])
        link_colors.append(yellow)

        # Työvoiman ulkopuolelta työlliseksi
        source.append(tyov_ulkop_offset + i)
        target.append(i + 1)
        value.append(df.iloc[i, 6])
        link_colors.append(yellow)

        # Työvoiman ulkopuolelta työttömäksi
        source.append(tyov_ulkop_offset + i)
        target.append(tyottomat_offset + i + 1)
        value.append(df.iloc[i, 7])
        link_colors.append(yellow)

    return labels, node_colors, source, target, value, link_colors, node_x, node_y


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def generate_sankey_figure(df, quarters):
    (
        labels,
        node_colors,
        source,
        target,
        value,
        link_colors,
        node_x,
        node_y,
    ) = generate_sankey_data(df)

    fig = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node={
                    "pad": 5,
                    "thickness": 15,
                    "label": labels,
                    "color": node_colors,
                    "hovertemplate": "Kokonaismäärä",
                },
                link={
                    "source": source,
                    "target": target,
                    "value": value,
                    "color": link_colors,
                    "hovertemplate": "Siirtymä",
                },
            ),
        ],
    )

    x_array = np.linspace(0, 1, len(quarters), endpoint=True)
    offset = 0.001
    x_array = x_array + offset

    annotations = [
        {
            "text": quarters[i],
            "textangle": 90,
            "xref": "x domain",
            "yref": "y domain",
            "x": x_array[i],
            "y": 1,
            "showarrow": False,
            "bgcolor": "white",
            "font": {"color": "red", "size": 15},
            "borderpad": 5,
        }
        for i in range(0, len(quarters))
    ]

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )  # annotations=annotations

    return fig
