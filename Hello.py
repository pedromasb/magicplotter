# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px
import numpy as np

LOGGER = get_logger(__name__)

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Let´s GO! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
**Probando Probando**
"""
)

upl_file = st.file_uploader('Choose a file')

if upl_file is not None:
    data = pd.read_csv(upl_file)
    st.write(data)

    cols = st.multiselect(
        "Choose columns", list(data.columns), [data.columns[1], data.columns[2]]
    )

    if len(cols)<2:
        st.error("Please select at least two columns.")
    else:    
        st.write(cols)

        col_size = st.multiselect(
        "Choose the column for points size",list(data.columns), data.columns[-1],max_selections=1)

        size_val = data[col_size].values.reshape(250,)

        colours = ['#ea5545','#25BDB0','#1F3440','#edbf33']

        colour_map = dict([(col, c) for col, c in zip(data[cols].columns,colours)])

        fig_scatter = px.scatter(data_frame=data, x=cols[0], y=cols[1:],
                                size=abs(np.round(size_val,2)*8),
                                width=800,
                                height=600,
                                color_discrete_map=colour_map)

        # For each feature, we change the name to that included in the dictionary labels_map
        # fig_scatter.for_each_trace(lambda t: t.update(name = labels_map[t.name]))


        # ----------------- From here it is only for formatting. No need to change anything -----------------


        # Choose the figure font
        font_dict=dict(family='Arial',
                      size=16,
                      color='black')

        # General figure formatting
        fig_scatter.update_layout(font=font_dict,  # font formatting
                                  plot_bgcolor='white',  # background color
                                  width=900,  # figure width
                                  height=600,  # figure height
                                  title={'text':'Interactive Scatter Plot','x':0.5,'font':{'size':24}},  # Title formatting
                                  legend_title='Data Collections')

        # x and y-axis formatting
        fig_scatter.update_yaxes(title_text='Feature',  # axis title
                                showline=True,  # add line at x=0
                                showticklabels=True,
                                showgrid=False,  # plot grid
                                gridcolor='lightgrey',
                                linecolor='black',  # line color
                                linewidth=1, # line size
                                ticks='outside',  # ticks outside/inside axis
                                tickfont=font_dict, # tick label font
                                mirror=True,  # add ticks to top/right axes
                                tickwidth=1,  # tick width
                                tickcolor='black')  # tick color

        fig_scatter.update_xaxes(title_text='x',
                                showline=True,
                                showticklabels=True,
                                showgrid=False,
                                gridcolor='lightgrey',
                                linecolor='black',
                                linewidth=1,
                                ticks='outside',
                                tickfont=font_dict,
                                mirror=True,
                                tickwidth=1,
                                tickcolor='black')

        st.plotly_chart(fig_scatter,theme=None)

        fig_html = fig_scatter.to_html()

        st.download_button(label='Download Figure in html',data=fig_html,file_name='plotly_figure.html')

else:
    st.markdown('## This is an example:')

    data = pd.read_csv('data/example_data.csv')
    # Dictionary (key:value) with the colour associated with each feature for the plot
    colour_map = {'y0': 'rgba(234, 85, 69,0.9)', 'y1': 'rgba(37, 189, 176, 0.9)', 'y2': 'rgba(31, 52, 64,0.9)', 'y3':'rgba(237, 191, 51,0.9)'}

    # Dictionary (key:value) with the label associated with each feature for the legend
    labels_map = {'y0': 'Data 0', 'y1': 'Data 1', 'y2': 'Data 2', 'y3':'Data 3'}

    fig_scatter = px.scatter(data_frame=data,x='x',y=['y0','y1','y2','y3'],
                            size=abs(np.round(data.iloc[:,-1],2)*8),
                            hover_name='obj',  # Name of the pop-up menu when we hover over a point
                            width=800,
                            height=600,
                            color_discrete_map=colour_map)

    # For each feature, we change the name to that included in the dictionary labels_map
    fig_scatter.for_each_trace(lambda t: t.update(name = labels_map[t.name]))

    # ----------------- From here it is only for formatting. No need to change anything -----------------

    # Choose the figure font
    font_dict=dict(family='Arial',
                  size=16,
                  color='black')

    # General figure formatting
    fig_scatter.update_layout(font=font_dict,  # font formatting
                              plot_bgcolor='white',  # background color
                              width=900,  # figure width
                              height=600,  # figure height
                              title={'text':'Interactive Scatter Plot','x':0.5,'font':{'size':24}},  # Title formatting
                              legend_title='Data Collections')

    # x and y-axis formatting
    fig_scatter.update_yaxes(title_text='Feature',  # axis title
                            showline=True,  # add line at x=0
                            showticklabels=True,
                            showgrid=False,  # plot grid
                            gridcolor='lightgrey',
                            linecolor='black',  # line color
                            linewidth=1, # line size
                            ticks='outside',  # ticks outside/inside axis
                            tickfont=font_dict, # tick label font
                            mirror=True,  # add ticks to top/right axes
                            tickwidth=1,  # tick width
                            tickcolor='black')  # tick color

    fig_scatter.update_xaxes(title_text='x',
                            showline=True,
                            showticklabels=True,
                            showgrid=False,
                            gridcolor='lightgrey',
                            linecolor='black',
                            linewidth=1,
                            ticks='outside',
                            tickfont=font_dict,
                            mirror=True,
                            tickwidth=1,
                            tickcolor='black')
    
    st.plotly_chart(fig_scatter,theme=None)

# except:
# print("An exception occurred")