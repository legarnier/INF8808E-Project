import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.subplots as sp
from itertools import count
import time

from IPython.display import display
import ipywidgets as widgets

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
                        x=0.15,
                        y=1.11,
                        text="Confidence Level: " + str(last_confidence_level) + "%",
                        showarrow=False,
                        font=dict(size=14),
                    ),
                    # Annotation text 2
                    go.layout.Annotation(
                        xref="paper",
                        yref="paper",
                        x=0.83,
                        y=1.11,
                        text="Volatility: " + str(last_volatility_level) + "%",
                        showarrow=False,
                        font=dict(size=14),
                    ),
                ]
            )

    


def add_forecasting(df):
    '''
        Add forecasting value to data

        Args:
            dataframe: The dataframe to process
        Returns:
            adding new value to current dataset related to forecasting. max min pretectid value, confidence level and Volatility
    '''
    # TODO : add new values to each row based on random formula
    
    # Specify the range for random values
  
    return df

def graphV1(df) : 
    # Define the main values, maximum values, and minimum values
    main_values = [1, 2, 3, 4, 5]
    max_values = [2, 3, 4, 5, 6]
    min_values = [0, 1, 2, 3, 4]

    x = dataframe['Time']
    main_values = dataframe['Latency']
    max_values = dataframe['Forecast max']
    max_values = dataframe['Forecast min']

    # Create the line graph with maximum and minimum values highlighted
    fig = go.Figure()

    # Add the main line
    fig.add_trace(go.Scatter(
        x=list(range(len(main_values))),
        y=main_values,
        mode='lines',
        name='Main Values'
    ))

    # Add the shaded region between the maximum and minimum values
    fig.add_trace(go.Scatter(
        x=list(range(len(max_values))),
        y=max_values,
        fill=None,
        mode='lines',
        line=dict(color='rgba(0,0,0,0)')
    ))

    fig.add_trace(go.Scatter(
        x=list(range(len(min_values))),
        y=min_values,
        fill='tonexty',
        mode='lines',
        name='Range',
        line=dict(color='rgba(0,0,0,0)')
    ))

    # Update layout
    fig.update_layout(
        title='Line Graph with Highlighted Range',
        xaxis=dict(title='X'),
        yaxis=dict(title='Y'),
        showlegend=True
    )

    # Display the graph
    fig.show()    



def graphV2(df):
    
    x = df['Time']
    y2 = df['Latency']
    y1 = df['Forecast max']
    y3 = df['Forecast min']


    mid_index = len(x) // 2

    x_half = x[:mid_index]
    y1_half = y1[:mid_index]
    y2_half = y2[:mid_index]
    y3_half = y3[:mid_index]
    last_confidence_level = round(df['Confidence Level'].iloc[mid_index-1],2)
    last_volatility_level = round(df['Volatility'].iloc[mid_index-1],2)


    # Print the first half of the dataframe
    print(df.head(mid_index) ,mid_index, df['Confidence Level'].iloc[mid_index-1])
    
    # create variable
    
    y_range = [0.5*min(min(y1), min(y2), min(y3)), 1.5*max(max(y1), max(y2), max(y3))]
    rang_y_linecolor=dict(color='rgba(0,0,0,0)')
    main_y_linecolor = dict(color='blue')
    fillcolor = 'lightblue'
    
    # Create traces for each line
    trace1 = go.Scatter(x=x_half, y=y1_half, mode='lines', name='Forecasting Max Latency', marker=dict(symbol='circle', size=8), fill = None,line = rang_y_linecolor)
    trace2 = go.Scatter(x=x_half, y=y2_half, mode='lines+markers', name='Total Current Latency',fill='tonexty', fillcolor = fillcolor , line = main_y_linecolor)
    trace3 = go.Scatter(x=x_half, y=y3_half, mode='lines', name='Forecasting Min Latency',fill='tonexty', fillcolor= fillcolor , line = rang_y_linecolor)

    # Create data list
    data = [trace1, trace2, trace3]

    data[0]['showlegend'] = False

    data[2]['name'] = 'Forecasting Range'

    # Create layout
    #layout = go.Layout(title='Line Chart', xaxis=dict(title='X'), yaxis=dict(title='Y', range=[0.5*min(min(y1), min(y2), min(y3)), 1.5*max(max(y1), max(y2), max(y3))]))
    # Create layout
    
    # Calculate the mid index


    layout = go.Layout(
    title={
        'text':'Forecast Latency',
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 30}  # Increase the font size to 24

        },
    xaxis=dict(title='Time',
               #tickangle=45, 
               tickmode='array',
               #tickvals=x, 
               tickvals=x[::2],  # Use every second value of x
               #range=[x[0], x[mid_index]]
               ticktext=[str(val) for val in x_half]
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
        yaxis_showticksuffix="all"  # or "first" or "last",
        ,#xaxis=dict(title='X', range=[x[0], x[mid_index]])
    )
    
    
    # Add annotations with curved box borders

    addBoxes(fig,last_confidence_level,last_volatility_level)
   
    # Display the chart
    
    
    
    fig.show()
    return fig
    f2 = go.FigureWidget(fig)

    


def graphV3(df):

    print(widgets.__version__)


    # Create a count variable to generate continuous x-axis values
    c = count()

    # Create subplots with two y-axes
    fig = sp.make_subplots(rows=1, cols=1, shared_xaxes=True)

    # Create the initial traces with empty data
    trace = go.Scatter(x=[], y=[], mode='lines', name='Real-Time Data')

    # Add the trace to the figure
    fig.append_trace(trace, row=1, col=1)



    # Create a figure widget
    fig_widget = go.FigureWidget(fig)

    # Create an output widget
    out = widgets.Output()

    # Define the update function
    def update_graph(_):
        with out:
            # Generate new data point
            x_val = next(c)
            y_val = x_val * 2

            # Append the new data point to the trace
            fig_widget.add_trace(go.Scatter(x=[x_val], y=[y_val], mode='lines', name='Real-Time Data'), row=1, col=1)

            # Limit the x-axis range to show only the latest half of the data
            fig_widget.update_xaxes(range=[max(0, x_val - 5), x_val + 1])

            # Update the figure
            fig_widget.show()

    # Create a button widget to trigger updates
    button = widgets.Button(description="Update Graph")

    # Register the update function to the button's on-click event
    button.on_click(update_graph)

    # Display the button and output widgets
    display(button, out)
    display(fig_widget)



def initial(dataframe):

    #print(dataframe[1])
    #preprocessing
    #print(dataframe)


    Quebec_dataframe = dataframe.loc[dataframe['Site'] == 'Quebec']

    #print(Quebec_dataframe)

    return (graphV2(Quebec_dataframe))

    #graphV3(Quebec_dataframe)







