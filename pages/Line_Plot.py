import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="MagicPlotter",
    page_icon="🚀"
)

st.title('MagicPlotter')
st.subheader('by Pedro Mas Buitrago &nbsp; [![pedro](https://img.shields.io/badge/%20Click_me!-red?style=social&logo=github&label=pedromasb&labelColor=grey)](https://pedromasb.github.io/)')

st.markdown('---')

st.markdown('## Line Plot')

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
            w = st.number_input('Figure width',value=900,min_value=100,max_value=1200,step=20)
        with cols_layout[1]:
            h = st.number_input('Figure height',value=600,min_value=100,max_value=1200,step=20)
        with cols_layout[2]:
            font_fam = st.selectbox("Choose font family", font_list)

        cols_layout = st.columns(4)
        with cols_layout[0]:
            c1 = st.text_input('Colour #1',value='rgba(234,85,69,0.7)')
        with cols_layout[1]:
            c2 = st.text_input('Colour #2',value='rgba(37,189,176,0.7)')
        with cols_layout[2]:
            c3 = st.text_input('Colour #3',value='rgba(31,52,64,0.7)')
        with cols_layout[3]:
            c4 = st.text_input('Colour #4',value='rgba(237,191,51,0.7)')

        cols_layout = st.columns(4)
        with cols_layout[0]:
            l1 = st.text_input('Label #1',value='Data 1')
        with cols_layout[1]:
            l2 = st.text_input('Label #2',value='Data 2')
        with cols_layout[2]:
            l3 = st.text_input('Label #3',value='Data 3')
        with cols_layout[3]:
            l4 = st.text_input('Label #4',value='Data 4')

        font_size = st.slider('Default font size',value=16,min_value=5,max_value=24)
        lw = st.slider('Line width',value=2,min_value=1,max_value=5)
        mk_size = st.slider('Marker size',value=8,min_value=1,max_value=20)
        
        legend_labels = ['x',l1,l2,l3,l4]
        labels_map = dict([(col, l) for col, l in zip(data[cols].columns,legend_labels)])

        colours = ['black',c1,c2,c3,c4]
        colour_map = dict([(col, c) for col, c in zip(data[cols].columns,colours)])

        fig = px.line(data_frame=data.sort_values(by=cols[0]), x=cols[0], y=cols[1:],
                                color_discrete_map=colour_map)
        
        fig.update_traces(line={'width': lw},marker={'size':mk_size})

        # For each feature, we change the name to that included in the dictionary labels_map
        fig.for_each_trace(lambda t: t.update(name = labels_map[t.name]))

        # ----------------- From here it is only for formatting. No need to change anything -----------------


        # Choose the figure font
        font_dict=dict(family=f'{font_fam}',
                        size=font_size,
                        color='black')

        # General figure formatting
        fig.update_layout(font=font_dict,  # font formatting
                                    plot_bgcolor='white',  # plot background color
                                    paper_bgcolor= 'white', # background color
                                    width=w,  # figure width
                                    height=h,  # figure height
                                    title={'text':f'{fig_title}','x':0.5,'font':{'size':24}},  # Title formatting
                                    legend_title='Data Collections')

        # x and y-axis formatting
        fig.update_yaxes(title_text=f'{y_label}',  # axis title
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
                                tickcolor='black',  # tick color
                                ticklen=10,
                                minor=dict(ticklen=5, tickcolor="black"),
                                title_standoff = 15)

        fig.update_xaxes(title_text=f'{x_label}',
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
                                tickcolor='black',
                                ticklen=10,
                                minor=dict(ticklen=5, tickcolor="black"),
                                title_standoff = 15)
        

        cols_layout = st.columns(4)
        with cols_layout[0]:
            x_rev = st.checkbox('Reverse X axis')
            if x_rev:
                fig.update_xaxes(autorange='reversed')
        with cols_layout[1]:
            y_rev = st.checkbox('Reverse Y axis')
            if y_rev:
                fig.update_yaxes(autorange='reversed')
        with cols_layout[2]:
            x_rev = st.checkbox('Log X axis')
            if x_rev:
                fig.update_xaxes(type="log")
        with cols_layout[3]:
            y_rev = st.checkbox('Log Y axis')
            if y_rev:
                fig.update_yaxes(type="log")
        
        cols_layout = st.columns(4)
        with cols_layout[0]:
            x_grid = st.checkbox('X grid')
            if x_grid:
                fig.update_xaxes(showgrid=True)
        with cols_layout[1]:
            y_grid = st.checkbox('Y grid')
            if y_grid:
                fig.update_yaxes(showgrid=True)
        with cols_layout[2]:
            x_mingrid = st.checkbox('X minor grid')
            if x_mingrid:
                fig.update_xaxes(minor=dict(ticklen=5, tickcolor="black",showgrid=True))
        with cols_layout[3]:
            y_mingrid = st.checkbox('Y minor grid')
            if y_mingrid:
                fig.update_yaxes(minor=dict(ticklen=5, tickcolor="black",showgrid=True))

        cols_layout = st.columns(4)
        with cols_layout[0]:
            xside = st.checkbox('Top X axis')
            if xside:
                fig.update_layout(xaxis={'side': 'top'})
        with cols_layout[1]:
            yside = st.checkbox('Right Y axis')
            if yside:
                fig.update_layout(yaxis={'side': 'right'})
        with cols_layout[2]:
            xrot = st.checkbox('Rotate X labels')
            if xrot:
                fig.update_xaxes(tickangle= -90)
        with cols_layout[3]:
            yrot = st.checkbox('Rotate Y labels')
            if yrot:
                fig.update_yaxes(tickangle= -90)

        pts = st.checkbox('Add data points')
        if pts:
            fig.update_traces(mode='markers+lines')

        st.plotly_chart(fig,theme=None)

        fig_html = fig.to_html()
        fig_pdf = fig.to_image(format='pdf')
        fig_png = fig.to_image(format='png',scale=5)

        cols_layout = st.columns(3)
        with cols_layout[0]:
            st.download_button(label='Download Figure as html',data=fig_html,file_name='plotly_figure.html')  
        with cols_layout[1]:
            st.download_button(label='Download Figure as pdf',data=fig_pdf,file_name='plotly_figure.pdf')  
        with cols_layout[2]:
            st.download_button(label='Download Figure as png',data=fig_png,file_name='plotly_figure.png') 

    if st.button('Click here to celebrate!',type="primary"):
        st.balloons()
        
# -------------------------- If not file is uploaded

else:
    st.text("")
    st.markdown('**Below you can find a demo. Choose your file to create your own plot!**')

    data = read_csv('data/example_data.csv')
    # Dictionary (key:value) with the colour associated with each feature for the plot
    colour_map = {'y0': 'rgba(234, 85, 69,0.9)', 'y1': 'rgba(37, 189, 176, 0.9)', 'y2': 'rgba(31, 52, 64,0.9)', 'y3':'rgba(237, 191, 51,0.9)'}

    # Dictionary (key:value) with the label associated with each feature for the legend
    labels_map = {'y0': 'Data 0', 'y1': 'Data 1', 'y2': 'Data 2', 'y3':'Data 3'}

    fig = px.line(data_frame=data.sort_values(by='x'),x='x',y=['y0','y1','y2','y3'],
                            hover_name='obj',  # Name of the pop-up menu when we hover over a point
                            width=800,
                            height=600,
                            color_discrete_map=colour_map)

    # For each feature, we change the name to that included in the dictionary labels_map
    fig.for_each_trace(lambda t: t.update(name = labels_map[t.name]))

    # ----------------- From here it is only for formatting. No need to change anything -----------------

    # Choose the figure font
    font_dict=dict(family='Arial',
                  size=16,
                  color='black')

    # General figure formatting
    fig.update_layout(font=font_dict,  # font formatting
                              plot_bgcolor='white',  # background color
                              width=900,  # figure width
                              height=600,  # figure height
                              title={'text':'Interactive Line Plot','x':0.5,'font':{'size':24}},  # Title formatting
                              legend_title='Data Collections')

    # x and y-axis formatting
    fig.update_yaxes(title_text='Feature',  # axis title
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
                            tickcolor='black',  # tick color
                            ticklen=10,
                            minor=dict(ticklen=5, tickcolor="black"))

    fig.update_xaxes(title_text='x',
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
                            tickcolor='black',
                            ticklen=10,
                            minor=dict(ticklen=5, tickcolor="black"))
    
    st.plotly_chart(fig,theme=None)