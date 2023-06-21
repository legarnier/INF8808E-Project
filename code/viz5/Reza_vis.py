import plotly.graph_objects as go
import pandas as pd
import numpy as np

def filter_groupby_time_city(df):
    '''
        Add forecasting value to data

        Args:
            dataframe: The dataframe to process
        Returns:
            only one total latency for each city per time
    '''
    # TODO : filter data by time and city and return filtered data
    #new_datafrom = df.groupby(['Site', 'Time'])['Total Latency','Forecast max',].first().reset_index()
    #new_datafram ={}
    #new_datafram['Forecast max avg w'] = df.groupby(['Site', 'Time'])['Latency'].mean().reset_index().rename(columns={'Latency': 'Average latency'})
    #new_datafram['Forecast max avg'] = df.groupby(['Site', 'Time'])['Forecast max'].mean().reset_index().rename(columns={'Latency': 'Average latency '})



    # Group by 'city' and calculate average of 'age'
    new_datafram = df.groupby(['Site', 'Time']).mean().reset_index()
    

    new_datafram = new_datafram[['Site','Time','Latency','Forecast max','Forecast min','Confidence Level','Volatility']]
    
    # Create three new columns based on grouped results
    #new_datafram = new_datafram.rename(columns={'age': 'average_age', 'salary': 'average_salary', 'height': 'average_height'})
    
    
    return new_datafram



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

    # create variable
    
    y_range = [0.5*min(min(y1), min(y2), min(y3)), 1.5*max(max(y1), max(y2), max(y3))]
    rang_y_linecolor=dict(color='rgba(0,0,0,0)')
    main_y_linecolor = dict(color='blue')
    fillcolor = 'lightblue'
    
    # Create traces for each line
    trace1 = go.Scatter(x=x, y=y1, mode='lines', name='Forecasting Max Latency', marker=dict(symbol='circle', size=8), fill = None,line = rang_y_linecolor)
    trace2 = go.Scatter(x=x, y=y2, mode='lines+markers', name='Total Current Latency',fill='tonexty', fillcolor = fillcolor , line = main_y_linecolor)
    trace3 = go.Scatter(x=x, y=y3, mode='lines', name='Forecasting Min Latency',fill='tonexty', fillcolor= fillcolor , line = rang_y_linecolor)

    # Create data list
    data = [trace1, trace2, trace3]

    
    
    # Create layout
    #layout = go.Layout(title='Line Chart', xaxis=dict(title='X'), yaxis=dict(title='Y', range=[0.5*min(min(y1), min(y2), min(y3)), 1.5*max(max(y1), max(y2), max(y3))]))
    # Create layout
    layout = go.Layout(
    title='Line Chart',
    xaxis=dict(title='Time',tickangle=45, tickmode='array', tickvals=x, ticktext=[str(val) for val in x]),
    yaxis=dict(title='Latency',range= y_range)
    )

    # Create figure
    fig = go.Figure(data=data, layout=layout)

    fig.update_layout(
        # on the y-axis
        yaxis_ticksuffix=" ms",
        # on the colorbar
        coloraxis_colorbar_ticksuffix="m",
        # To specify which tick should have suffix
        yaxis_showticksuffix="all"  # or "first" or "last"
    )
    # Display the chart
    fig.show()
    
    
    

dataframe = pd.read_csv('../../data/dataset.csv')

#print(dataframe[1])
#preprocessing
dataframe = filter_groupby_time_city(dataframe)

#print(dataframe)


Quebec_dataframe = dataframe.loc[dataframe['Site'] == 'Quebec']

#print(Quebec_dataframe)

graphV2(Quebec_dataframe)







