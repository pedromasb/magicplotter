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

            &nbsp;

            ''')

st.info(''' 
            **Streamlit Data Privacy**          
          
            Streamlit Cloud is [SOC 2 Type 1 compliant](https://blog.streamlit.io/streamlit-cloud-is-now-soc-2-type-1-compliant/), which means they have been audited and
            found to have appropriate systems in place to ensure the security of the system (protecting against unauthorized access) and the confidentiality of the information 
            processed by the system (ensuring that sensitive data is accessed only by authorized individuals) at a specific point in time.

            Streamlit has a server-client structure. The server executes the Python code and the client is a browser, typically on a different computer from the server.
            When you upload a file to the app, the data is sent from the client to the server and contained in a BytesIO buffer in Python memory (i.e. RAM, not disk).
            As files are stored in memory, they get deleted immediately as soon as they're not needed anymore. This means Streamlit removes a file from memory when:

            - The user uploads another file, replacing the original one.
            - The user clears the file uploader.
            - The user closes the browser tab where they uploaded the file.

            Additional details can be found in their [Trust and Security](https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started/trust-and-security) policy.
                    
            ''')