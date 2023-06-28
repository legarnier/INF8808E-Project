import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.subplots as sp
from itertools import count
import time

from IPython.display import display
import ipywidgets as widgets
import hover_template

def addBoxes(fig,last_confidence_level,last_volatility_level) : 
        fig.update_layout(
                shapes=[
                    # Annotation box 1
                    go.layout.Shape(
                        type="rect",
                        xref="paper",
                        yref="paper",
                        x0=0.1,
                        y0=1.05,
                        x1=0.3,
                        y1=1.15,
                        fillcolor="lightblue",
                        line=dict(color="black", width=1),
                    ),
                    # Annotation box 2
                    go.layout.Shape(
                        type="rect",
                        xref="paper",
                        yref="paper",
                        x0=0.7,
                        y0=1.05,
                        x1=0.9,
                        y1=1.15,
                        fillcolor="lightblue",
                        line=dict(color="black", width=1),
                    ),
                ],
                annotations=[
                    # Annotation text 1
                    go.layout.Annotation(
                        xref="paper",
                        yref="paper",
                        x=0.11,
                        y=1.11,
                        text="Confidence Level: " + str(last_confidence_level) + "%",
                        showarrow=False,
                        font=dict(size=14),
                    ),
                    # Annotation text 2
                    go.layout.Annotation(
                        xref="paper",
                        yref="paper",
                        x=0.85,
                        y=1.11,
                        text="Volatility: " + str(last_volatility_level) + "%",
                        showarrow=False,
                        font=dict(size=14),
                    ),
                ]
            )




def graphV2(df):
    
    x = df['Time']
    y_main = df['Latency']
    y_max = df['Forecast max']
    y_min = df['Forecast min']


    mid_index = len(x) // 2

    x_half = x[:mid_index]
    y_max_half = y_max[:mid_index]
    y_main_half = y_main[:mid_index]
    y_min_half = y_min[:mid_index]
    
    confidence_level = df['Confidence Level']
    volatility_level = df['Volatility']
    
    last_confidence_level = round(confidence_level.iloc[mid_index-1],2)
    last_volatility_level = round(volatility_level.iloc[mid_index-1],2)
    
   
    
    hover_text = hover_template.hover_vis5_forcasting_range(y_min, y_main, y_max, confidence_level, volatility_level)

   

    # Print the first half of the dataframe
    #print(df.head(mid_index) ,mid_index, df['Confidence Level'].iloc[mid_index-1])
    
    # create variable
    
    y_range = [0.5*min(min(y_max), min(y_main), min(y_min)), 1.5*max(max(y_max), max(y_main), max(y_min))]
    rang_y_linecolor=dict(color='rgba(0,0,0,0)')
    main_y_linecolor = dict(color='blue')
    fillcolor = 'lightblue'
    
    # Create traces for each line
    trace1 = go.Scatter(x=x, y=y_max, mode='lines', marker=dict(symbol='circle', size=8), fill = None,line = rang_y_linecolor, hoverinfo="skip")
    trace2 = go.Scatter(x=x, y=y_main, mode='lines+markers', name='Total Current Latency',fill='tonexty', fillcolor = fillcolor , 
                        line = main_y_linecolor,
                        customdata=list(zip(y_max, y_min, confidence_level, volatility_level)),
                        hoverlabel=dict(bgcolor='lightblue'),  # here you can set the hover background color
                        hovertemplate=hover_text
                        )
    trace3 = go.Scatter(x=x, y=y_min, mode='lines', name='Forecasting Min Latency',fill='tonexty', fillcolor= fillcolor , line = rang_y_linecolor,hoverinfo="skip")

    # Create data list
    data = [trace1, trace2, trace3]

    data[0]['showlegend'] = False

    data[2]['name'] = 'Forecasting Range'

    # Create layout
    #layout = go.Layout(title='Line Chart', xaxis=dict(title='X'), yaxis=dict(title='Y', range=[0.5*min(min(y_max), min(y_main), min(y_min)), 1.5*max(max(y_max), max(y_main), max(y_min))]))
    # Create layout
    
    # Calculate the mid index


    layout = go.Layout(
    title={
        'text':'',
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 30},  # Increase the font size to 24,
         'y': 0.995  # Adjust the y coordinate to position the title higher
        },
    xaxis=dict(title='Time',
               #tickangle=45, 
               tickmode='array',
               #tickvals=x, 
               tickvals=x[::2],  # Use every second value of x
               #range=[x[0], x[mid_index]]
               ticktext=[str(val) for val in x]
               ),
    yaxis=dict(title='Latency',range= y_range)
    )
    
    

    # Create figure
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
        title={
        'x': 0.5,  # Adjust the vertical position of the title if needed
        },
        # on the y-axis
        yaxis_ticksuffix=" ms",
        # on the colorbar
        coloraxis_colorbar_ticksuffix="m",
        # To specify which tick should have suffix
        yaxis_showticksuffix="all",
        hovermode="x",
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )# or "first" or "last",
        ,#xaxis=dict(title='X', range=[x[0], x[mid_index]])
    )
    
    
   
   
    # Display the chart    
  
    
    
    x_half = x[1:mid_index+1]
    y_max_half = y_max[1:mid_index+1]
    y_main_half = y_main[1:mid_index+1]
    y_min_half = y_min[1:mid_index+1]
    
    last_confidence_level = round(df['Confidence Level'].iloc[mid_index],2)
    last_volatility_level = round(df['Volatility'].iloc[mid_index],2)
    # Re-layout the graph
    
    #fig.data[0].y = y_max_half
    #fig.data[1].y = y_main_half
    #fig.data[2].y = y_min_half
   
    #fig.update_layout(hovermode="x unified")
  
   
    # Add annotations with box borders
    addBoxes(fig,last_confidence_level,last_volatility_level)

    fig.update_layout()

    #fig.show()
    return fig

    


def graphV3(df):


    import plotly.graph_objects as go

    # your data
    x_values = [1, 2, 3, 4, 5]  # these would be your 'x' values
    y_values = [10, 15, 7, 10, 12]  # these would be your 'y' values
    y_mins = [8, 13, 5, 8, 10]  # these would be your minimum 'y' values
    y_maxs = [12, 17, 9, 12, 14]  # these would be your maximum 'y' values

    # create hover text for main line
    hover_text = ['Value: {}<br>Max: {}<br>Min: {}'.format(y, y_max, y_min) 
                for y, y_max, y_min in zip(y_values, y_maxs, y_mins)]

    # create trace for line (main values)
    trace0 = go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines+markers',
        name='Value',
        line=dict(color='rgb(0,0,0)'),
        hovertemplate=hover_text,
        hoverinfo='x+text',
    )

    # create trace for fill (min and max values)
    trace1 = go.Scatter(
        x=x_values+x_values[::-1],  # x, then x reversed
        y=y_maxs+y_mins[::-1],  # upper, then lower reversed
        fill='toself',
        fillcolor='rgba(190,190,190,0.5)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False,
    )

    # layout
    layout = go.Layout(
        yaxis=dict(title='Values'),
        xaxis=dict(title='X values'),
        title='Line chart with Min-Max shaded',
    )

    # create figure and add traces
    fig = go.Figure(layout=layout)
    fig.add_trace(trace1)  # add fill before line
    fig.add_trace(trace0)  # add line

    # show figure
    fig.show()





def initial(dataframe):



    Quebec_dataframe = dataframe.loc[dataframe['Site'] == 'Quebec']

    #graphV3(Quebec_dataframe)

    return (graphV2(Quebec_dataframe))








