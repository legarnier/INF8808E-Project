import plotly.express as px
import preprocess
import pandas as pd
from datetime import date
from dash import html, dcc


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

def get_empty_figure(): # show nothing on the second chart when there is no click on the bubble chart
    fig = px.line(x=[0,0], y=[0,0])
    fig.add_annotation(text='No data to display.<br> Select a bubble for more information.', xref='paper', yref='paper', showarrow=False) # src to center the text: https://codepen.io/etpinard/pen/WpmNEo
    fig.update_layout(dragmode = False, xaxis = {'visible': False, 'showticklabels': False}, yaxis = {'visible': False, 'showticklabels': False}, plot_bgcolor='rgb(243, 243, 243)')
                      
    return fig

# draw line chart for each application type
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


#read data from csv file
dataframe = pd.read_csv('../data/dataset.csv')

# Get the vis2
vis2_bubble_df = preprocess.bubble_chart_df(dataframe)
fig2_bubble = buble_chart(vis2_bubble_df)
fig2_line = get_empty_figure()

viz2_layout = html.Div(children=[
                html.Div(className='filter-container', children=[
                    html.Label('Date range', style={
                            'padding-top': '2%', 'padding-left': '2%'}), 
                    html.Div([
                        dcc.DatePickerRange( # filter the charte based on the date (from june 1st to june 5th)
                            id='filter_date',
                            start_date_placeholder_text="Start Period",
                            end_date_placeholder_text="End Period",
                            calendar_orientation='vertical',
                            min_date_allowed=date(
                                2023, 6, 1),
                            max_date_allowed=date(
                                2023, 6, 5),
                            initial_visible_month=date(
                                2023, 6, 5),
                            end_date=date(
                                2023, 6, 5),
                            style={
                                'padding': '2%'}
                        ),
                        html.Div(id='output-container-date-picker-range')
                    ]),
                    html.Label('Protocol', style={'padding-top': '2%', 'padding-left': '2%'}),
                    html.Div([ # filter the charte based on the protocols
                        dcc.Dropdown(['All', 'HTTP', 'HTTPS', 'TCP', 'UDP', 'ICMP', 'TWAMP'], 'All', id='filter_protocol', style={
                        'width': '100px'}),
                        html.Div(id='output'),
                    ], style={'padding': '2%', 'display': 'inline-flex'}),
                ]),
                html.Div(className='vis2-container' ,children=[
                    dcc.Graph(
                        id = 'fig2-bubble',
                        className = 'vis2-graph',
                        figure = fig2_bubble
                    ),
                    dcc.Graph(
                        id = 'fig2-line',
                        className = 'vis2-graph',
                        figure = fig2_line
                        ),
                ]),
])
