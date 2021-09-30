import plotly.graph_objects as go
import streamlit as st
import numpy as np


@st.cache(suppress_st_warning=True)
def generate_sankey_data(df, quarters):
    # Lasketaan nodejen alkupaikat
    rows_n = (
        len(df) + 1
    )  # Rivien määrä. Lasketaan offset. +1 koska alussa "haamurivi" ekalle lähteelle
    tyottomat_offset = rows_n
    tyov_ulkop_offset = tyottomat_offset + rows_n

    # Color palette:
    green = np.array([0, 132, 80])
    red = np.array([184, 29, 19])
    yellow = np.array([239, 183, 0])
    shader = [1.2, 1, 0.8, 0.6]
    opacity = 0.5

    greens = ["rgba" + str(tuple(list(green * shade) + [opacity])) for shade in shader]
    reds = ["rgba" + str(tuple(list(red * shade) + [opacity])) for shade in shader]
    yellows = [
        "rgba" + str(tuple(list(yellow * shade) + [opacity])) for shade in shader
    ]

    qs = [s[4:6] for s in quarters]
    q_mapper = {"Q1": 0, "Q2": 1, "Q3": 2, "Q4": 3}

    green = "rgba(0,132,80, 0.4)"
    red = "rgba(184,29,19, 0.4)"
    yellow = "rgba(239,183,0, 0.4)"

    # darker2_green = 0.50
    # darker1_green = "rgba(0,99,60, 0.4)"
    # darkest_green =

    # Labelit, värit ja paikat nodeille
    labels = ["Työlliset"] + [None for i in range(1, rows_n)]
    # node_colors = [green for i in range(0, rows_n)]
    node_colors = [greens[q_mapper[q]] for q in qs]
    node_x = list(np.linspace(0, 1, rows_n, endpoint=True))
    node_y = [0 for i in range(0, rows_n)]

    labels = labels + ["Työttömät"] + [None for i in range(1, rows_n)]
    node_colors = node_colors + [
        reds[q_mapper[q]] for q in qs
    ]  # [red for i in range(0, rows_n)]
    node_x = node_x + list(np.linspace(0, 1, rows_n, endpoint=True))
    node_y = node_y + [0.5 for i in range(0, rows_n)]

    labels = labels + ["Työvoiman ulkopuolella"] + [None for i in range(1, rows_n)]
    node_colors = node_colors + [yellows[q_mapper[q]] for q in qs]
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
        # link_colors.append(green)
        link_colors.append(greens[q_mapper[qs[i]]])

        # Työllisestä työttömäksi
        source.append(i)
        target.append(tyottomat_offset + i + 1)
        value.append(df.iloc[i, 1])
        # link_colors.append(green)
        link_colors.append(greens[q_mapper[qs[i]]])

        # Työttömästä työlliseksi
        source.append(tyottomat_offset + i)
        target.append(i + 1)
        value.append(df.iloc[i, 3])
        # link_colors.append(red)
        link_colors.append(reds[q_mapper[qs[i]]])

        # Työttömänä pysyneet
        source.append(tyottomat_offset + i)
        target.append(tyottomat_offset + i + 1)
        value.append(df.iloc[i, 4])
        # link_colors.append(red)
        link_colors.append(reds[q_mapper[qs[i]]])

        # Työllisestä työvoiman ulkopuolelle
        source.append(i)
        target.append(tyov_ulkop_offset + i + 1)
        value.append(df.iloc[i, 2])
        # link_colors.append(green)
        link_colors.append(greens[q_mapper[qs[i]]])

        # Työttömästä työvoiman ulkopuolelle
        source.append(tyottomat_offset + i)
        target.append(tyov_ulkop_offset + i + 1)
        value.append(df.iloc[i, 5])
        # link_colors.append(red)
        link_colors.append(reds[q_mapper[qs[i]]])

        # Työvoiman ulkopuolella pysyneet
        source.append(tyov_ulkop_offset + i)
        target.append(tyov_ulkop_offset + i + 1)
        value.append(df.iloc[i, 8])
        # link_colors.append(yellow)
        link_colors.append(yellows[q_mapper[qs[i]]])

        # Työvoiman ulkopuolelta työlliseksi
        source.append(tyov_ulkop_offset + i)
        target.append(i + 1)
        value.append(df.iloc[i, 6])
        # link_colors.append(yellow)
        link_colors.append(yellows[q_mapper[qs[i]]])

        # Työvoiman ulkopuolelta työttömäksi
        source.append(tyov_ulkop_offset + i)
        target.append(tyottomat_offset + i + 1)
        value.append(df.iloc[i, 7])
        # link_colors.append(yellow)
        link_colors.append(yellows[q_mapper[qs[i]]])

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
    ) = generate_sankey_data(df, quarters)

    fig = go.Figure(
        data=[
            go.Sankey(
                valueformat=".0f",
                valuesuffix=" (1k hlö)",
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
