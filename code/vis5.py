import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.subplots as sp
from itertools import count
import time

from IPython.display import display
import ipywidgets as widgets
import hover_template

from dash import html, dcc

#I add layout of viz5 here to make apppy easier to read
#First I have a div to have the dropdown for name of cities.
card_layout = html.Div([
            # BEGIN LEFT PART
            html.Div([
                dcc.Dropdown(
                    [{"label": html.Span("Quebec",
                                        style={'color': 'blue'}),
                    "value": "Quebec"},
                    {"label": html.Span("Ontario",
                                        style={'color': 'red'}),
                    "value": "Ontario"},
                    {"label": html.Span("Manitoba",
                                        style={'color': 'green'}),
                    "value": "Manitoba"}
                    ],
                    'Quebec',
                    id='viz5_places',
                    searchable=False,
                    clearable=False,
                )
            ],
            style={'width': '49%', 'display': 'inline-block'}),
            # END LEFT PART

            # BEGIN RIGHT PART
            html.Div(["Select each city to see the forecasting values for Latency"], style={'width': '49%',
                    'float': 'right', 'display': 'inline-block'})
            # END RIGHT PART


        ], style={
            'padding': '10px 5px'
        })
                                                        
#In this function I add two box at the top of my graph to show two value: [last_confidence_level,last_volatility_level ]
#I create a simaple shape by go.layout.shape and then put value there
def addBoxes(fig,last_confidence_level,last_volatility_level,main_color,color_light) : 
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
                        fillcolor=color_light,
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
                        fillcolor=color_light,
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
        
def update_vis5(df,city):
    
    
    #I have three diffrent city to show their latency forecast during time. for better visualization
    #I create three difrent color for ecah city
    # First I created the color then an array to have all colors
    light_red = 'lightpink'
    light_green =  'lightgreen'
    light_blue = 'lightblue'
    
    colors = [
    {"name": "Quebec", "color": 'blue', "color_light": light_blue},
    {"name": "Ontario", "color": 'red', "color_light": light_red},
    {"name": "Manitoba", "color": 'green', "color_light": light_green}
    ]

    #Create a simple dataframe because it is easier to find value there by panda data structure:D
    colors_df = pd.DataFrame(colors)
    
    
    #I choose the color here based on city value. As I told before I selected a speceif color or ecah city.
    main_color = colors_df.query(f"name == '{city}'")['color'].values[0]
    color_light = colors_df.query(f"name == '{city}'")['color_light'].values[0]

    
    # For my graph I need to show the main current latency, then highlight between max an min forecast value to show the range.
    # based on my dataset, 
    x = df['Time']
    y_main = df['Latency']
    y_max = df['Forecast max']
    y_min = df['Forecast min']

    x_len = len(x)

    
    confidence_level = df['Confidence Level']
    volatility_level = df['Volatility']
    
    last_confidence_level = round(confidence_level.iloc[x_len-1],2)
    last_volatility_level = round(volatility_level.iloc[x_len-1],2)

    #For hover tempalte  we need some values, so I created a array to use it in then
    hover_text = hover_template.hover_vis5_forcasting_range(y_min, y_main, y_max, confidence_level, volatility_level)

    # To have a better veiw of my graph I decieded to have adynamic range of bigest value and minest value then use a coeffiecnt of that value.
    #I mean instead of draw graph from shortest to largest value show my favourite range
    y_range = [0.8*min(min(y_max), min(y_main), min(y_min)), 1.2*max(max(y_max), max(y_main), max(y_min))]
    x_range = [min(x), max(x)]

    rang_y_linecolor=dict(color='rgba(0,0,0,0)')
    
    #Assign the color selected before. I have a set of colro for each city
    main_y_linecolor = dict(color= main_color)
    fillcolor = color_light
    
   
    #Here I create the layout.
    layout = go.Layout(
        height=700,
        title={
            'text':'',
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 30},  # Increase the font size to 30,
            'y': 0.995 , # Adjust the y coordinate to position the title higher
            'x': 0.5,  # Adjust the vertical position of the title if needed
            },
        xaxis=dict(title='Time',
                #tickangle=45, 
                tickmode='array',
                #tickvals=x, 
                tickvals=x[::2],  # Use every second value of x
                #range=[x[0], x[mid_index]]
                ticktext=[str(val) for val in x]
                ),
        yaxis=dict(title='Latency',range= y_range),
        
            # on the y-axis
            yaxis_ticksuffix=" ms", #add suffix to each y value index
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
            
    # Create figure
    fig = go.Figure(layout=layout)
    
    
    # Add annotations with box borders
    addBoxes(fig,last_confidence_level,last_volatility_level,main_color,color_light)
    
        
    # Create traces for each line 
    # As i told before I have three difrent values. main latency, max and min values.
    # I use fill properties to fullfil my goal. I put fill = none for max value . "tonexty" for middle value then "tonexty" for min value.
    trace1 = go.Scatter(x=x, y=y_max, mode='lines', marker=dict(symbol='circle', size=8), fill = None,line = rang_y_linecolor, hoverinfo="skip")
    trace2 = go.Scatter(x=x, y=y_main, mode='lines+markers', name='Total Current Latency',fill='tonexty', fillcolor = fillcolor , 
                        line = main_y_linecolor,
                        customdata=list(zip(y_max, y_min, confidence_level, volatility_level)),
                        hoverlabel=dict(bgcolor=color_light),  # here you can set the hover background color
                        hovertemplate=hover_text
                        )
    trace3 = go.Scatter(x=x, y=y_min, mode='lines', name='Forecasting Min Latency',fill='tonexty', fillcolor= fillcolor , line = rang_y_linecolor,hoverinfo="skip")

    # Here I try to show that last 10 percent of the graph are preticted so I draw  dash line graph for last 10 percent of the graph.
    x_index = int(x_len * 0.90)
    trace2_1 = go.Scatter(x=x[x_index:],
                          y=y_main[x_index:],
                          hoverinfo="skip",
                          showlegend=False,  # This trace will not appear in the legend
                          line=dict(width=4, color='white', dash='dash'))

    # Create data list
    data = [trace1, trace2, trace3]
    data[0]['showlegend'] = False
    data[2]['name'] = 'Forecasting Range'


    # Display the chart    
    
    # add traces to figure
    fig.add_traces(trace1)  # add fill before line
    fig.add_traces(trace2)  # add fill before line
    fig.add_traces(trace3)  # add fill before line


    # add traces to figure
    fig.add_traces(trace2_1)  # add fill before line
    fig.update_xaxes(range=x_range)  # set the x-axis range

    return fig
