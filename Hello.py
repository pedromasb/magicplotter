import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px
import numpy as np

LOGGER = get_logger(__name__)

st.set_page_config(
    page_title="MagicPlotter",
    page_icon="🚀",
)

st.write("# Let´s GO! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
**Probando Probando**
"""
)

@st.cache_data()
def read_csv(file):
    data = pd.read_csv(file)
    return data
               
upl_file = st.file_uploader('Choose a file')

if upl_file is not None:
    data = read_csv(upl_file)
    st.write(data)

    cols = st.multiselect(
        "Choose columns", list(data.columns),  [data.columns[1], data.columns[2]], max_selections=5
    )

    if len(cols)<2:
        st.error("Please select at least two columns.")

    else:    
        st.write(cols)

        font_list = ["Arial","Courier New", "Open Sans"]

        fig_title = st.text_input('Figure title',value='', placeholder = 'Enter a title')

        cols_layout = st.columns(2)
        with cols_layout[0]:
            x_label = st.text_input('X label','X')
        with cols_layout[1]:
            y_label = st.text_input('Y label','Y')

        cols_layout = st.columns(3)
        with cols_layout[0]:
            w = st.number_input('Figure width',value=900,min_value=100,max_value=1200)
        with cols_layout[1]:
            h = st.number_input('Figure height',value=600,min_value=100,max_value=1200)
        with cols_layout[2]:
            font_fam = st.selectbox("Choose columns", font_list)

        cols_layout = st.columns(4)
        with cols_layout[0]:
            c1 = st.text_input('Colour #1',value='rgba(234,85,69,0.7)')
        with cols_layout[1]:
            c2 = st.text_input('Colour #2',value='rgba(37,189,176,0.7)')
        with cols_layout[2]:
            c3 = st.text_input('Colour #3',value='rgba(31,52,64,0.7)')
        with cols_layout[3]:
            c4 = st.text_input('Colour #4',value='rgba(237,191,51,0.7)')

        font_size = st.slider('Default font size',value=16,min_value=5,max_value=24)

        colours = ['black',c1,c2,c3,c4]
        colour_map = dict([(col, c) for col, c in zip(data[cols].columns,colours)])

        fig_scatter = px.scatter(data_frame=data, x=cols[0], y=cols[1:],
                                size=np.ones(len(data))*15,
                                color_discrete_map=colour_map)
        
        fig_scatter.update_traces(marker={'size': 15})

        # ----------------- From here it is only for formatting. No need to change anything -----------------


        # Choose the figure font
        font_dict=dict(family=f'{font_fam}',
                        size=font_size,
                        color='black')

        # General figure formatting
        fig_scatter.update_layout(font=font_dict,  # font formatting
                                    plot_bgcolor='white',  # plot background color
                                    paper_bgcolor= 'white', # background color
                                    width=w,  # figure width
                                    height=h,  # figure height
                                    title={'text':f'{fig_title}','x':0.5,'font':{'size':24}},  # Title formatting
                                    legend_title='Data Collections')

        # x and y-axis formatting
        fig_scatter.update_yaxes(title_text=f'{y_label}',  # axis title
                                showline=True, 
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

        fig_scatter.update_xaxes(title_text=f'{x_label}',
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

        cols_layout = st.columns(4)
        with cols_layout[0]:
            x_rev = st.checkbox('Reverse X axis')
            if x_rev:
                fig_scatter.update_xaxes(autorange='reversed')
        with cols_layout[1]:
            y_rev = st.checkbox('Reverse Y axis')
            if y_rev:
                fig_scatter.update_yaxes(autorange='reversed')
        with cols_layout[2]:
            x_grid = st.checkbox('X Grid')
            if x_grid:
                fig_scatter.update_xaxes(showgrid=True)
        with cols_layout[3]:
            x_grid = st.checkbox('Y Grid')
            if x_grid:
                fig_scatter.update_yaxes(showgrid=True)

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