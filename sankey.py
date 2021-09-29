import plotly.graph_objects as go
import streamlit as st

@st.cache(suppress_st_warning=True)
def generate_sankey_data(df):
    # Lasketaan nodejen alkupaikat
    rows_n = (
        len(df) + 1
    )  # Rivien määrä. Lasketaan offset. +1 koska alussa "haamurivi" ekalle lähteelle
    tyottomat_offset = rows_n
    tyov_ulkop_offset = tyottomat_offset + rows_n

    # Labelit nodeille
    labels = ["Työlliset" for i in range(0, rows_n)]
    labels = labels + ["Työttömät" for i in range(0, rows_n)]
    labels = labels + ["Työvoiman ulkopuolella" for i in range(0, rows_n)]

    # Color palette:
    green = "rgba(0,132,80, 0.4)"
    red = "rgba(184,29,19, 0.4)"
    yellow = "rgba(239,183,0, 0.4)"

    # Värit nodeille
    node_color_map = {
        "Työlliset": green,
        "Työttömät": red,
        "Työvoiman ulkopuolella": yellow,
    }
    node_colors = [node_color_map[node_type] for node_type in labels]

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

    return labels, node_colors, source, target, value, link_colors

@st.cache(suppress_st_warning=True)
def generate_sankey_figure(df):
    labels, node_colors, source, target, value, link_colors = generate_sankey_data(df)

    fig = go.Figure(
        data=[
            go.Sankey(
                node={"pad": 10, "label": labels, "color": node_colors},
                link={
                    "source": source,
                    "target": target,
                    "value": value,
                    "color": link_colors,
                },
            )
        ]
    )

    fig.update_layout(
        title_text="Työvoiman liikkeet kvartaalista x kvartaaliin y", font_size=10
    )

    return fig
