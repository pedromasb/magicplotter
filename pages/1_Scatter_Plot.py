import plotly.graph_objects as go
import streamlit as st

import mp_core as mp

mp.page_header("Scatter Plot")
df = mp.load_data()

if df is None:
    data = mp.read_example("data/example_data.csv")
    fig = go.Figure()
    for i, col in enumerate(["y0", "y1", "y2", "y3"]):
        fig.add_scatter(x=data["x"], y=data[col], mode="markers", name=f"Data {i}",
                        marker=dict(size=12, color=mp.hex_to_rgba(mp.PALETTE[i], 0.7),
                                    line=dict(width=0.7, color="white")))
    mp.demo(fig, "Interactive Scatter Plot", "x", "Feature")
    st.stop()

cols = mp.select_columns(
    df, 2, mp.MAX_SERIES + 1,
    "Choose columns: the first one is used for the X axis, the rest are plotted on the Y axis.",
)
if cols is None:
    st.stop()

style = mp.style_sidebar()
series = mp.series_controls(cols[1:], default_alpha=0.7)

with st.sidebar:
    st.header("Markers")
    mk_size = st.slider("Marker size", value=12, min_value=2, max_value=30)
    c = st.columns(2)
    edge_w = c[0].slider("Edge width", value=0.7, min_value=0.0, max_value=3.0, step=0.1)
    edge_color = c[1].selectbox("Edge color", ["white", "black", "grey", "lightgrey"])
    symbol = st.selectbox("Marker symbol", ["circle", "square", "diamond", "triangle-up", "cross", "x"])

# WebGL keeps large point clouds responsive.
Trace = go.Scattergl if len(df) > 5000 else go.Scatter
fig = go.Figure()
for s in series:
    fig.add_trace(Trace(
        x=df[cols[0]], y=df[s.column], mode="markers", name=s.label,
        marker=dict(size=mk_size, color=s.color, symbol=symbol, line=dict(width=edge_w, color=edge_color)),
        hovertemplate=f"<b>{s.label}</b><br>{cols[0]}: %{{x}}<br>{s.column}: %{{y}}<extra></extra>",
    ))

mp.finish(fig, style)
mp.celebrate()
