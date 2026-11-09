import plotly.graph_objects as go
import streamlit as st

import mp_core as mp

POINTS = {"All": "all", "Outliers": "outliers", "None": False}

mp.page_header("Violin Plot")
df = mp.load_data()

if df is None:
    data = mp.read_example("data/example_data.csv")
    fig = go.Figure()
    for i, col in enumerate(["y0", "y1", "y2", "y3"]):
        fig.add_violin(y=data[col], name=f"Data {i}", points="all", pointpos=-1.8,
                       line=dict(width=2, color=mp.PALETTE[i]), fillcolor=mp.hex_to_rgba(mp.PALETTE[i], 0.4),
                       marker=dict(color=mp.hex_to_rgba(mp.PALETTE[i], 0.4), line=dict(width=1, color=mp.PALETTE[i])),
                       box_visible=True, meanline_visible=True)
    mp.demo(fig, "Interactive Violin Plot", "", "Value")
    st.stop()

cols = mp.select_columns(df, 1, mp.MAX_SERIES, "Choose columns")
if cols is None:
    st.stop()

style = mp.style_sidebar(x_label="", y_label="Value")
series = mp.series_controls(cols, default_alpha=0.4)

with st.sidebar:
    st.header("Violins")
    c = st.columns(2)
    lw = c[0].slider("Violin line width", value=2.0, min_value=0.5, max_value=5.0, step=0.5)
    mk_lw = c[1].slider("Marker edge width", value=1.0, min_value=0.0, max_value=5.0, step=0.5)
    c = st.columns(2)
    spmode = c[0].selectbox("Span mode", ["soft", "hard"])
    pts = POINTS[c[1].selectbox("Points", list(POINTS))]
    c = st.columns(2)
    show_box = c[0].checkbox("Inner box", value=True)
    show_mean = c[1].checkbox("Mean line", value=True)
    side = st.selectbox("Side", ["both", "positive", "negative"])

fig = go.Figure()
for s in series:
    fig.add_violin(
        y=df[s.column], name=s.label, points=pts, pointpos=-1.8 if side == "both" else 0,
        spanmode=spmode, side=side, line=dict(width=lw, color=s.solid), fillcolor=s.color,
        marker=dict(color=s.color, line=dict(width=mk_lw, color=s.solid)),
        box_visible=show_box, meanline_visible=show_mean,
    )

mp.finish(fig, style, options=("x_rev", "y_rev", "y_log", "y_grid", "y_mgrid",
                               "x_mirror", "y_mirror", "x_rot", "y_rot"))
mp.celebrate()
