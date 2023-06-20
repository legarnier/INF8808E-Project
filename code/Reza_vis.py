import plotly.graph_objects as go
import pandas as pd
import numpy as np

def filter_just_time_latency(df):
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

    print(new_datafram)
    
    
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


dataframe = pd.read_csv('dataset.csv')

#print(dataframe[1])
#preprocessing
dataframe = filter_just_time_latency(dataframe)

#print(dataframe)

dataframe = add_forecasting(dataframe)

#print(dataframe)








# Define the main values, maximum values, and minimum values
main_values = [1, 2, 3, 4, 5]
max_values = [2, 3, 4, 5, 6]
min_values = [0, 1, 2, 3, 4]

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
#fig.show()