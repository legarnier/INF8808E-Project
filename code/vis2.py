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

def get_empty_figure():
    fig = px.line(x=[0,0], y=[0,0])
    fig.add_annotation(text='No data to display.<br> Select a bubble for more information.', xref='paper', yref='paper', showarrow=False) # src to center the text: https://codepen.io/etpinard/pen/WpmNEo
    fig.update_layout(dragmode = False, xaxis = {'visible': False, 'showticklabels': False}, yaxis = {'visible': False, 'showticklabels': False}, plot_bgcolor='rgb(243, 243, 243)')
                      
    return fig

def line_chart(df, application_type):
    fig = px.line(df, x = "Time", y = "Latency")
    fig.update_layout(
        title=f'Latency for {application_type} over time',
        xaxis=dict(
            title='Time',
        ),
        yaxis=dict(
            title='Latency',
        ),
        paper_bgcolor='rgb(243, 243, 243)',
        plot_bgcolor='rgb(243, 243, 243)',
    )
    return fig
