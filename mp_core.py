"""Shared building blocks for every MagicPlotter page.

Each page only contains the code that is specific to its chart type; data
loading, styling widgets, axis options, rendering and export live here.
"""

from __future__ import annotations

import io
from dataclasses import dataclass

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------

PALETTE = ["#EA5545", "#25BDB0", "#1F3440", "#EDBF33"]
FONTS = ["Arial", "Courier New", "Open Sans", "Helvetica", "Times New Roman"]
MAX_SERIES = len(PALETTE)

AUTHOR_BADGE = (
    "by Pedro Mas Buitrago &nbsp; "
    "[![pedro](https://img.shields.io/badge/%20Click_me!-red?style=social"
    "&logo=github&label=pedromasb&labelColor=grey)](https://pedromasb.github.io/)"
)

# Client-side modebar export: the camera icon downloads a 2x SVG at no server cost.
CHART_CONFIG = {
    "displaylogo": False,
    "toImageButtonOptions": {"format": "svg", "filename": "magicplotter_figure", "scale": 2},
}

# Every axis option a page can offer: key -> (checkbox label, axis, update kwargs).
AXIS_OPTIONS = {
    "x_rev": ("Reverse X axis", "x", {"autorange": "reversed"}),
    "y_rev": ("Reverse Y axis", "y", {"autorange": "reversed"}),
    "x_log": ("Log X axis", "x", {"type": "log"}),
    "y_log": ("Log Y axis", "y", {"type": "log"}),
    "x_grid": ("X grid", "x", {"showgrid": True}),
    "y_grid": ("Y grid", "y", {"showgrid": True}),
    "x_mgrid": ("X minor grid", "x", {"minor_showgrid": True}),
    "y_mgrid": ("Y minor grid", "y", {"minor_showgrid": True}),
    "x_mirror": ("Top X axis ticks", "x", {"mirror": "ticks"}),
    "y_mirror": ("Right Y axis ticks", "y", {"mirror": "ticks"}),
    "x_rot": ("Rotate X labels", "x", {"tickangle": -90}),
    "y_rot": ("Rotate Y labels", "y", {"tickangle": -90}),
}
ALL_AXIS_OPTIONS = tuple(AXIS_OPTIONS)


# ----------------------------------------------------------------------------
# Page scaffolding
# ----------------------------------------------------------------------------

def page_header(title: str, intro: str | None = None) -> None:
    st.set_page_config(page_title=f"MagicPlotter · {title}", page_icon="🚀", layout="wide")
    st.title("MagicPlotter")
    st.subheader(AUTHOR_BADGE)
    st.markdown(
        f"""
        ---
        ## {title}

        - Use the box below to select your own `csv` or `txt` file.
        - This tool supports comma, space or custom separated files, with or without headers.
        - Once the file is uploaded, adjust the settings until the data is displayed correctly in the table.
        """
    )
    if intro:
        st.markdown(intro)


def celebrate() -> None:
    if st.button("Click here to celebrate!", type="primary"):
        st.balloons()


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------

@st.cache_data(show_spinner=False, max_entries=20)
def _parse(raw: bytes, header: int | None, sep: str, quotechar: str) -> pd.DataFrame:
    engine = "python" if len(sep) > 1 and sep != r"\s+" else "c"
    df = pd.read_csv(io.BytesIO(raw), header=header, sep=sep, quotechar=quotechar or '"', engine=engine)
    # Plotly and the label/colour maps work with string column names.
    df.columns = [str(c) for c in df.columns]
    return df


@st.cache_data(show_spinner=False)
def read_example(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_data() -> pd.DataFrame | None:
    """File uploader + parsing options. Returns the parsed DataFrame or None."""
    upl_file = st.file_uploader("Choose a file", type=["csv", "txt", "tsv", "dat"])
    if upl_file is None:
        return None

    c = st.columns(4)
    has_header = c[0].checkbox("File has headers", value=True)
    sep_opt = c[1].selectbox("Separator character", ["comma separated", "space separated", "custom character"])
    quote = c[2].text_input("Text qualifier", value='"', max_chars=1)
    sep = {"comma separated": ",", "space separated": r"\s+"}.get(sep_opt)
    if sep is None:
        sep = c[3].text_input("Custom separator character", value=",") or ","

    try:
        df = _parse(upl_file.getvalue(), 0 if has_header else None, sep, quote)
    except Exception as exc:  # malformed files should not crash the page
        st.error(f"Could not read the file with these settings: {exc}")
        return None

    if df.empty:
        st.error("The file contains no data rows.")
        return None

    st.dataframe(df.head(), width="stretch")
    return df


def select_columns(df: pd.DataFrame, min_n: int, max_n: int, label: str) -> list[str] | None:
    cols = list(df.columns)
    if len(cols) < min_n:
        st.error(f"This plot needs at least {min_n} column(s); the file has {len(cols)}.")
        return None
    chosen = st.multiselect(label, cols, cols[:min_n], max_selections=max_n)
    if len(chosen) < min_n:
        st.error(f"Please select at least {min_n} column(s).")
        return None
    return chosen


# ----------------------------------------------------------------------------
# Styling
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Style:
    title: str = ""
    font: str = "Arial"
    font_size: int = 16
    x_label: str = "X"
    y_label: str = "Y"
    width: int = 840
    height: int = 540


@dataclass(frozen=True)
class Series:
    column: str
    label: str
    color: str        # rgba with the chosen opacity
    solid: str        # same colour, fully opaque (edges, lines)


def hex_to_rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha:g})"


def style_sidebar(x_label: str = "X", y_label: str = "Y") -> Style:
    with st.sidebar:
        st.header("Figure")
        c = st.columns(2)
        title = c[0].text_input("Figure title", placeholder="Enter a title")
        font = c[1].selectbox("Font family", FONTS)
        c = st.columns(2)
        xl = c[0].text_input("X label", x_label)
        yl = c[1].text_input("Y label", y_label)
        c = st.columns(2)
        w = c[0].number_input("Figure width", value=840, min_value=100, max_value=2000, step=20)
        h = c[1].number_input("Figure height", value=540, min_value=100, max_value=2000, step=20)
        size = st.slider("Default font size", value=16, min_value=5, max_value=24)
    return Style(title, font, size, xl, yl, int(w), int(h))


def series_controls(columns: list[str], default_alpha: float = 0.7) -> list[Series]:
    """Colour picker + legend label for each selected column."""
    alpha = st.slider("Fill opacity", 0.0, 1.0, default_alpha, 0.05)
    out = []
    grid = st.columns(MAX_SERIES)
    for i, col in enumerate(columns):
        with grid[i % MAX_SERIES]:
            color = st.color_picker(f"Colour #{i + 1}", PALETTE[i % len(PALETTE)], key=f"color_{i}_{col}")
            label = st.text_input(f"Label #{i + 1}", value=col, key=f"label_{i}_{col}")
        out.append(Series(col, label, hex_to_rgba(color, alpha), hex_to_rgba(color, 1)))
    return out


def apply_style(fig: go.Figure, style: Style, legend_title: str = "Data Collections") -> go.Figure:
    font = dict(family=style.font, size=style.font_size, color="black")
    fig.update_layout(
        template="simple_white",
        font=font,
        plot_bgcolor="white",
        paper_bgcolor="white",
        width=style.width,
        height=style.height,
        title=dict(text=style.title, x=0.5, xanchor="center", font_size=24),
        legend_title_text=legend_title,
        margin=dict(t=80 if style.title else 40),
    )
    axis = dict(
        showline=True,
        zeroline=False,
        showgrid=False,
        gridcolor="lightgrey",
        linecolor="black",
        linewidth=1,
        ticks="outside",
        tickfont=font,
        mirror=True,
        tickwidth=1,
        tickcolor="black",
        ticklen=10,
        minor=dict(ticks="outside", ticklen=5, tickcolor="black", gridcolor="#eeeeee", showgrid=False),
        title_standoff=8,
    )
    fig.update_xaxes(title_text=style.x_label, **axis)
    fig.update_yaxes(title_text=style.y_label, **axis)
    return fig


def axis_options(fig: go.Figure, options: tuple[str, ...] = ALL_AXIS_OPTIONS, n_cols: int = 4) -> None:
    """Render a checkbox grid for the requested axis options and apply them."""
    with st.expander("Axis options", expanded=True):
        grid = st.columns(n_cols)
        for i, key in enumerate(options):
            label, axis, kwargs = AXIS_OPTIONS[key]
            if grid[i % n_cols].checkbox(label, key=f"axis_{key}"):
                (fig.update_xaxes if axis == "x" else fig.update_yaxes)(**kwargs)


# ----------------------------------------------------------------------------
# Rendering & export
# ----------------------------------------------------------------------------

def show_chart(fig: go.Figure) -> None:
    st.plotly_chart(fig, theme=None, width="content", config=CHART_CONFIG)


@st.cache_data(show_spinner=False, max_entries=10)
def _to_image(fig_json: str, fmt: str) -> bytes:
    import plotly.io as pio

    return pio.from_json(fig_json).to_image(format=fmt)


@st.cache_data(show_spinner=False, max_entries=10)
def _to_html(fig_json: str) -> str:
    import plotly.io as pio

    return pio.from_json(fig_json).to_html(include_plotlyjs="cdn", full_html=True, config=CHART_CONFIG)


def export_buttons(fig: go.Figure) -> None:
    """Download buttons. Files are only generated when a button is clicked."""
    fig_json = fig.to_json()
    c = st.columns([0.2, 0.2, 0.2, 0.4])
    c[0].download_button("Download as HTML", lambda: _to_html(fig_json),
                         file_name="magicplotter_figure.html", mime="text/html")
    c[1].download_button("Download as PDF", lambda: _to_image(fig_json, "pdf"),
                         file_name="magicplotter_figure.pdf", mime="application/pdf")
    c[2].download_button("Download as PNG", lambda: _to_image(fig_json, "png"),
                         file_name="magicplotter_figure.png", mime="image/png")


def finish(fig: go.Figure, style: Style, options: tuple[str, ...] = ALL_AXIS_OPTIONS,
           legend_title: str = "Data Collections") -> None:
    """Common tail of every page: style, axis options, chart, downloads."""
    apply_style(fig, style, legend_title)
    axis_options(fig, options)
    show_chart(fig)
    export_buttons(fig)


def demo(fig: go.Figure, title: str, x_label: str, y_label: str) -> None:
    """Render a cached demo figure (shown when no file is uploaded)."""
    st.markdown("**Below you can find a demo. Choose your file to create your own plot!**")
    apply_style(fig, Style(title=title, x_label=x_label, y_label=y_label))
    show_chart(fig)
