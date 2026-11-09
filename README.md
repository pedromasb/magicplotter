# MagicPlotter

Use this Streamlit app to create interactive visualizations from your data in minutes.

Check it out on &nbsp; [![st badge](https://img.shields.io/badge/MagicPlotter-lightgrey?style=flat-square&logo=streamlit&labelColor=white)](https://magicplotter.streamlit.app/)

Below you can find a demo on how to use the app.

https://github.com/pedromasb/magicplotter/assets/112410947/bcc65c63-e419-46a6-b1bd-82887c850654

## Running the app locally

```bash
git clone https://github.com/pedromasb/magicplotter.git
cd magicplotter
pip install -r requirements.txt
streamlit run Hello.py
```

PDF/PNG export uses [Kaleido](https://github.com/plotly/Kaleido), which needs a Chrome/Chromium
installation. If none is available, run `plotly_get_chrome` once (or install Chromium with your
package manager). On Streamlit Community Cloud this is handled by `packages.txt`.

The camera icon in each chart's toolbar always downloads a high-resolution SVG directly in the
browser, no server-side rendering required.
