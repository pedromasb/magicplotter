import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="MagicPlotter",
    page_icon="🚀")

st.title('MagicPlotter')
st.subheader('by Pedro Mas Buitrago &nbsp; [![pedro](https://img.shields.io/badge/%20Click_me!-red?style=social&logo=github&label=pedromasb&labelColor=grey)](https://pedromasb.github.io/)')

st.markdown('''
            ---
            #### Welcome! 

            **MagicPlotter** is a tool developed to help the user create and share interactive visualizations
            in record time and without the need to write any code.

            1. Choose the desired type of figure you want to create in the left sidebar.
            2. Import your data from a `csv` or `txt` file without effort.
            3. Play with the plethora of different options and create the perfect visualization.
            4. Export your figure in a static or interactive way.

            With **MagicPlotter**, you will save up to **500 lines of code per visualization**. Interactive data-sharing has never been easier!





            ''')