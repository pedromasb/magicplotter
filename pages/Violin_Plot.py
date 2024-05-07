import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="MagicPlotter",
    page_icon="🚀"
)

st.title('MagicPlotter')
st.subheader('by Pedro Mas Buitrago &nbsp; [![pedro](https://img.shields.io/badge/%20Click_me!-red?style=social&logo=github&label=pedromasb&labelColor=grey)](https://pedromasb.github.io/)')

st.markdown('---')

st.markdown('## Histogram')

@st.cache_data()
def read_csv(file,header=0,sep=','):
    data = pd.read_csv(file,header=header,sep=sep)
    return data
               
upl_file = st.file_uploader('Choose a file')

if upl_file is not None:

    sep_list = ['comma separated','space separated']
        
    cols_layout = st.columns(2)

    with cols_layout[0]:
        header_bool = st.checkbox('File has headers')
    with cols_layout[1]:
        sep_opt = st.selectbox("Separator character", sep_list)
        
    if (header_bool) & (sep_opt=='comma separated'):
        data = read_csv(upl_file)

    if (header_bool) & (sep_opt=='space separated'):
        data = read_csv(upl_file,header=0,sep=r'\s+')

    elif (~header_bool) & (sep_opt=='comma separated'):
        data = read_csv(upl_file,header=None,sep=',')
    
    elif (~header_bool) & (sep_opt=='space separated'):
        data = read_csv(upl_file,header=None,sep=r"\s+")

    st.write(data)

    cols = st.multiselect(
        "Choose columns", list(data.columns),  [data.columns[1], data.columns[2]], max_selections=4
    )

    if len(cols)<1:
        st.error("Please select at least one column.")

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
            c1 = st.text_input('Color #1',value='rgba(234,85,69,0.4)')
        with cols_layout[1]:
            c2 = st.text_input('Color #2',value='rgba(37,189,176,0.4)')
        with cols_layout[2]:
            c3 = st.text_input('Color #3',value='rgba(31,52,64,0.4)')
        with cols_layout[3]:
            c4 = st.text_input('Color #4',value='rgba(237,191,51,0.4)')

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
        lw = st.slider('Violin line width',value=2,min_value=1,max_value=5)
        mk_lw = st.slider('Marker line width',value=1,min_value=0,max_value=5)

        spanmode_list = ['soft','hard']
        pts_list = ['all',False,'outliers']

        cols_layout = st.columns(2)
        with cols_layout[0]:
            spmode = st.selectbox("Span mode", spanmode_list)
        with cols_layout[1]:
            pts = st.selectbox("Points", pts_list)

        legend_labels = [l1,l2,l3,l4]

        colours = [c1,c2,c3,c4]
        colours_noalpha = [c.replace(c.split(',')[3],'1)') for c in colours]

        fig_violin = go.Figure()

        for i, var in enumerate(cols):
            fig_violin.add_trace(go.Violin(y=data[var],
                                        name=legend_labels[i],
                                        points=pts,
                                        pointpos=-1.8,
                                        line_color=colours_noalpha[i],
                                        spanmode=spmode,
                                        line=dict(width=lw),
                                        marker=dict(color=colours[i],line=dict(width=mk_lw,color=colours_noalpha[i])),
                                        fillcolor=colours[i],
                                        box_visible=True,
                                        meanline_visible=True))
            
        # ----------------- From here it is only for formatting. No need to change anything -----------------

        # Choose the figure font
        font_dict=dict(family=f'{font_fam}',
                        size=font_size,
                        color='black')

        # General figure formatting
        fig_violin.update_layout(font=font_dict,  # font formatting
                                    plot_bgcolor='white',  # plot background color
                                    paper_bgcolor= 'white', # background color
                                    width=w,  # figure width
                                    height=h,  # figure height
                                    title={'text':f'{fig_title}','x':0.5,'font':{'size':24}},  # Title formatting
                                    legend_title='Data Collections')

        # x and y-axis formatting
        fig_violin.update_yaxes(title_text=f'{y_label}',  # axis title
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

        fig_violin.update_xaxes(title_text=f'{x_label}',
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
                fig_violin.update_xaxes(autorange='reversed')
        with cols_layout[1]:
            y_rev = st.checkbox('Reverse Y axis')
            if y_rev:
                fig_violin.update_yaxes(autorange='reversed')
        with cols_layout[2]:
            y_rev = st.checkbox('Log Y axis')
            if y_rev:
                fig_violin.update_yaxes(type="log")
        with cols_layout[3]:
            x_grid = st.checkbox('X grid')
            if x_grid:
                fig_violin.update_xaxes(showgrid=True)        
        
        cols_layout = st.columns(4)
        with cols_layout[0]:
            y_grid = st.checkbox('Y grid')
            if y_grid:
                fig_violin.update_yaxes(showgrid=True)
        with cols_layout[1]:
            y_mingrid = st.checkbox('Y minor grid')
            if y_mingrid:
                fig_violin.update_yaxes(minor=dict(ticklen=5, tickcolor="black",showgrid=True))
        with cols_layout[2]:
            xside = st.checkbox('Top X axis')
            if xside:
                fig_violin.update_layout(xaxis={'side': 'top'})
        with cols_layout[3]:
            yside = st.checkbox('Right Y axis')
            if yside:
                fig_violin.update_layout(yaxis={'side': 'right'})
        
        cols_layout = st.columns(2)
        with cols_layout[0]:
            xrot = st.checkbox('Rotate X labels')
            if xrot:
                fig_violin.update_xaxes(tickangle= -90)
        with cols_layout[1]:
            yrot = st.checkbox('Rotate Y labels')
            if yrot:
                fig_violin.update_yaxes(tickangle= -90)

        st.plotly_chart(fig_violin,theme=None)

        fig_html = fig_violin.to_html()
        fig_pdf = fig_violin.to_image(format='pdf')
        fig_png = fig_violin.to_image(format='png',scale=5)

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

    variables = ['y0','y1','y2','y3']

    # Dictionary (key:value) with the colour associated with each feature for the plot
    colour_map = ['rgba(234, 85, 69, 0.4)','rgba(37, 189, 176, 0.4)','rgba(31, 52, 64, 0.4)','rgba(237, 191, 51, 0.4)']
    colours = ['#ea5545','#25BDB0','#1F3440','#edbf33']

    # Dictionary (key:value) with the label associated with each feature for the legend
    labels_map = {'y0': 'Data 0', 'y1': 'Data 1', 'y2': 'Data 2', 'y3':'Data 3'}

    fig_violin = go.Figure()

    for i, var in enumerate(variables):
        fig_violin.add_trace(go.Violin(y=data[var],
                                    name=var,
                                    points='all',
                                    pointpos=-1.8,
                                    line_color=colours[i],
                                    fillcolor=colour_map[i],
                                    box_visible=True,
                                    meanline_visible=True))

    # For each feature, we change the name to that included in the dictionary labels_map
    # fig.for_each_trace(lambda t: t.update(name = labels_map[t.name]))

    # ----------------- From here it is only for formatting. No need to change anything -----------------

    # Choose the figure font
    font_dict=dict(family='Arial',
                  size=16,
                  color='black')

    # General figure formatting
    fig_violin.update_layout(font=font_dict,  # font formatting
                              plot_bgcolor='white',  # background color
                              width=900,  # figure width
                              height=600,  # figure height
                              title={'text':'Interactive Violin Plot','x':0.5,'font':{'size':24}},  # Title formatting
                              legend_title='Data Collections')

    # x and y-axis formatting
    fig_violin.update_yaxes(title_text='Count',  # axis title
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

    fig_violin.update_xaxes(title_text='x',
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
    
    st.plotly_chart(fig_violin,theme=None)