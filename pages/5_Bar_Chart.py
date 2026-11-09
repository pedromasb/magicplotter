import plotly.graph_objects as go
import streamlit as st

import mp_core as mp

SORTS = ["Descending total", "Ascending total", "File order", "Alphabetical"]

mp.page_header("Bar Chart")
df = mp.load_data()


def sort_rows(data, cat, values, how):
    if how == "File order":
        return data
    if how == "Alphabetical":
        return data.sort_values(cat)
    total = data[values].sum(axis=1)
    return data.loc[total.sort_values(ascending=how.startswith("Asc")).index]


if df is None:
    data = sort_rows(mp.read_example("data/example_data_red.csv"), "obj", ["y0", "y1", "y2", "y3"],
                     "Descending total")
    fig = go.Figure()
    for i, col in enumerate(["y0", "y1", "y2", "y3"]):
        fig.add_bar(x=data["obj"], y=data[col], name=f"Data {i}",
                    marker=dict(color=mp.hex_to_rgba(mp.PALETTE[i], 0.7), line=dict(width=1.5, color="black")))
    fig.update_layout(barmode="stack")
    mp.demo(fig, "Interactive Bar Chart", "", "Value")
    st.stop()

cols = mp.select_columns(
    df, 2, mp.MAX_SERIES + 1,
    "Choose columns: the first one holds the categories, the rest are the bar values.",
)
if cols is None:
    st.stop()

style = mp.style_sidebar(x_label="", y_label="Value")
series = mp.series_controls(cols[1:], default_alpha=0.7)

c = st.columns(3)
bmode = c[0].selectbox("Bar mode", ["group", "stack", "overlay", "relative"])
horizontal = c[1].selectbox("Orientation", ["Vertical", "Horizontal"]) == "Horizontal"
order = c[2].selectbox("Sort bars", SORTS)

with st.sidebar:
    st.header("Bars")
    c = st.columns(2)
    lw = c[0].slider("Edge width", value=1.5, min_value=0.0, max_value=5.0, step=0.5)
    lc = c[1].color_picker("Edge color", "#000000")
    show_values = st.checkbox("Show values on bars")

data = sort_rows(df, cols[0], [s.column for s in series], order)
if horizontal:  # first category at the top
    data = data.iloc[::-1]

fig = go.Figure()
for s in series:
    cat, val = data[cols[0]].astype(str), data[s.column]
    fig.add_bar(
        x=val if horizontal else cat, y=cat if horizontal else val,
        orientation="h" if horizontal else "v", name=s.label,
        marker=dict(color=s.color, line=dict(width=lw, color=lc)),
        texttemplate=("%{x:.3s}" if horizontal else "%{y:.3s}") if show_values else None,
    )
fig.update_layout(barmode=bmode)
if not horizontal:
    fig.update_xaxes(categoryorder="array", categoryarray=list(data[cols[0]].astype(str)))

mp.finish(fig, style, options=("x_rev", "y_rev", "y_log" if not horizontal else "x_log",
                               "x_grid", "y_grid", "x_mirror", "y_mirror", "x_rot", "y_rot"))
mp.celebrate()
