import plotly.graph_objects as go
import streamlit as st

import mp_core as mp

mp.page_header("Line Plot")
df = mp.load_data()

if df is None:
    data = mp.read_example("data/example_data.csv").sort_values("x")
    fig = go.Figure()
    for i, col in enumerate(["y0", "y1", "y2", "y3"]):
        fig.add_scatter(x=data["x"], y=data[col], mode="lines", name=f"Data {i}",
                        text=data["obj"], line=dict(width=2, color=mp.hex_to_rgba(mp.PALETTE[i], 0.9)))
    mp.demo(fig, "Interactive Line Plot", "x", "Feature")
    st.stop()

cols = mp.select_columns(
    df, 2, mp.MAX_SERIES + 1,
    "Choose columns: the first one is used for the X axis, the rest are plotted on the Y axis.",
)
if cols is None:
    st.stop()

style = mp.style_sidebar()
series = mp.series_controls(cols[1:], default_alpha=0.9)

with st.sidebar:
    st.header("Lines")
    c = st.columns(2)
    lw = c[0].slider("Line width", value=2.0, min_value=0.5, max_value=6.0, step=0.5)
    shape = c[1].selectbox("Line shape", ["linear", "spline", "hv", "vh"])
    dash = st.selectbox("Line style", ["solid", "dash", "dot", "dashdot"])
    show_pts = st.checkbox("Add data points")
    if show_pts:
        c = st.columns(2)
        mk_size = c[0].slider("Marker size", value=8, min_value=1, max_value=20)
        mk_lw = c[1].slider("Marker edge width", value=0.0, min_value=0.0, max_value=3.0, step=0.1)
        edge_color = st.selectbox("Marker edge color", ["white", "black", "grey", "lightgrey"])

data = df.sort_values(cols[0])
Trace = go.Scattergl if len(data) > 5000 else go.Scatter
fig = go.Figure()
for s in series:
    trace = Trace(
        x=data[cols[0]], y=data[s.column], name=s.label,
        mode="lines+markers" if show_pts else "lines",
        line=dict(width=lw, color=s.color, dash=dash,
                  shape=shape if Trace is go.Scatter else "linear"),
        hovertemplate=f"<b>{s.label}</b><br>{cols[0]}: %{{x}}<br>{s.column}: %{{y}}<extra></extra>",
    )
    if show_pts:
        trace.marker = dict(size=mk_size, color=s.color, line=dict(width=mk_lw, color=edge_color))
    fig.add_trace(trace)

mp.finish(fig, style)
mp.celebrate()
