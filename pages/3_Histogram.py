import plotly.graph_objects as go
import streamlit as st

import mp_core as mp

NORMS = {"None (count)": None, "Probability": "probability", "Percent": "percent",
         "Density": "density", "Probability density": "probability density"}

mp.page_header("Histogram")
df = mp.load_data()

if df is None:
    data = mp.read_example("data/example_data.csv")
    fig = go.Figure()
    for i, col in enumerate(["y0", "y1", "y2", "y3"]):
        fig.add_histogram(x=data[col], name=f"Data {i}",
                          marker=dict(color=mp.hex_to_rgba(mp.PALETTE[i], 0.5), line=dict(width=1.5, color="black")))
    fig.update_layout(barmode="overlay")
    mp.demo(fig, "Interactive Histogram", "x", "Count")
    st.stop()

cols = mp.select_columns(df, 1, mp.MAX_SERIES, "Choose columns")
if cols is None:
    st.stop()

style = mp.style_sidebar(x_label="Value", y_label="Count")
series = mp.series_controls(cols, default_alpha=0.6)

c = st.columns(4)
bmode = c[0].selectbox("Bar mode", ["overlay", "group", "stack"])
norm = NORMS[c[1].selectbox("Normalize", list(NORMS))]
horizontal = c[2].selectbox("Orientation", ["Vertical", "Horizontal"]) == "Horizontal"
nbins = c[3].number_input("Number of bins (0 = auto)", value=0, min_value=0, max_value=500, step=5)

with st.sidebar:
    st.header("Bars")
    c = st.columns(2)
    lw = c[0].slider("Edge width", value=1.5, min_value=0.0, max_value=5.0, step=0.5)
    lc = c[1].color_picker("Edge color", "#000000")
    cumulative = st.checkbox("Cumulative")

fig = go.Figure()
for s in series:
    values = df[s.column]
    fig.add_histogram(
        **({"y": values} if horizontal else {"x": values}),
        name=s.label, histnorm=norm, nbinsx=None if horizontal else (nbins or None),
        nbinsy=(nbins or None) if horizontal else None, cumulative_enabled=cumulative,
        marker=dict(color=s.color, line=dict(width=lw, color=lc)),
    )
fig.update_layout(barmode=bmode, bargap=0.02)

mp.finish(fig, style, options=tuple(k for k in mp.ALL_AXIS_OPTIONS if k != "x_log"))
mp.celebrate()
