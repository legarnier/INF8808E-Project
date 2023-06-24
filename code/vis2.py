import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math

def buble_chart(df):
    
    fig = px.scatter(df, x='Frequency', y='Average latency', color='Application type', size='Average packet loss')
    fig.update_layout(
        title='Average Latency per application type',
        xaxis=dict(
            title='Frequency',
            gridcolor='white',
            type='log',
            gridwidth=2,
        ),
        yaxis=dict(
            title='Average latency',
            gridcolor='white',
            gridwidth=2,
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
    )
    return fig

def line_chart(df):
    pass