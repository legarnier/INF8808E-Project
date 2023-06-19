import plotly.graph_objects as go
import pandas as pd



dataframe = pd.read_csv('dataset.csv')

#preprocessing




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
fig.show()