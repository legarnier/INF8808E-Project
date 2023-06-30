from dash import html, dcc
import pandas as pd
import plotly.express as px
import numpy as np
import pandas as pd


df = pd.read_csv(('../data/dense_dataset.csv'))


######## Heatmap ########

def extract_heatmap_data(df, site, typ):
    heatmap_data = df.loc[(df['Site'] == site) & (df['Type'] == typ)]
    heatmap_data = pd.pivot_table(
        heatmap_data, index='Time', columns='Protocol', values='Latency')
    date_range = pd.date_range(
        start=df['Time'].min(), end=df['Time'].max(), freq='10s')
    heatmap_data = heatmap_data.groupby(np.arange(len(heatmap_data))//10).max()

    heatmap_data['Time'] = date_range
    heatmap_data = heatmap_data.set_index('Time')
    heatmap_data.columns = ['HTTP', 'HTTPS', 'ICMP', 'TCP', 'TWAMP', 'UDP']
    return heatmap_data


def update_heatmap(df, place_name, type_name):

    # Create the heatmap figure
    fig = px.imshow(extract_heatmap_data(df,
                                         place_name,
                                         type_name).T,
                    color_continuous_scale=[[0, 'rgb(247, 233, 235)'],
                                            [0.5, 'rgb(247, 233, 235)'],
                                            [0.75, 'rgb(204, 167, 173)'],
                                            [1, 'rgb(173, 16, 60)']
                                            ],
                    origin='upper',
                    aspect='auto')

    fig.update_xaxes({
        'showgrid': False,  # thin lines in the background
        'zeroline': False,  # thick line at x=0
        'visible': True,  # numbers below
    })

    fig.update_yaxes({
        'showgrid': False,  # thin lines in the background
        'zeroline': False,  # thick line at x=0
        'visible': True,  # numbers below
    })

    fig.update_traces(hovertemplate="<span><b>Latency:</b> %{z:.2f} ms<br><b>Time:</b> %{x|%H:%M}</span><extra></extra>")

    return fig

######## Line ########


def get_empty_figure():
    fig = px.line({})
    return fig


def update_line(df, clickData, zoom_level, place, typ):

    max_time_range = (df['Time'].max() - df['Time'].min()).seconds

    time_range = int(max_time_range/10**zoom_level)

    if clickData is not None:
        protocol_name = clickData['points'][0]['y']
        selected_time = pd.to_datetime(clickData['points'][0]['x'])
    else:
        selected_time = df['Time'][0]
        protocol_name = 'HTTP'
    dataline = df.loc[(df['Site'] == place) &
                      (df['Type'] == typ) &
                      (df['Protocol'] == protocol_name) &
                      (df['Time'] >= selected_time-pd.Timedelta(seconds=time_range)) &
                      (df['Time'] <= selected_time+pd.Timedelta(seconds=time_range))]
    fig = px.line(dataline, x='Time', y='Latency',
                  title=protocol_name)
    fig.update_traces(hovertemplate="<span>Time: %{x|%H:%M}<br>Latency: %{y:.2f} ms</span><extra></extra>")

    return fig


def get_empty_figure():
    fig = px.line({})
    return fig


######## Layout ########
layout = html.Div([
    html.Div([
        # BEGIN LEFT PART
        html.Div([
            dcc.Dropdown(
                [{"label": html.Span("Quebec",
                                     style={'color': 'blue','font-family': 'oswald'}),
                  "value": "Quebec"},
                 {"label": html.Span("Ontario",
                                     style={'color': 'red','font-family': 'oswald'}),
                  "value": "Ontario"},
                 {"label": html.Span("Manitoba",
                                     style={'color': 'green','font-family': 'oswald'}),
                  "value": "Manitoba"}
                 ],
                'Quebec',
                id='place',
                searchable=False,
                clearable=False,
            ),
            dcc.RadioItems(
                [{"label": html.Span("Application",
                                     style={'color': 'red'}),
                  "value": "app"},
                 {"label": html.Span("Network",
                                     style={'color': 'blue'}),
                  "value": "network"}],
                'app',
                id='type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ],
            style={'width': '49%', 'display': 'inline-block','font-family': 'oswald'}),
        # END LEFT PART

        # BEGIN RIGHT PART
        html.Div(["Click on the heatmap and select a zoom level"], style={'width': '49%',
                 'float': 'right', 'display': 'inline-block','font-family': 'oswald'})
        # END RIGHT PART


    ], style={
        'padding': '10px 5px'
    }),

    # BEGIN LEFT PART
    html.Div([
        dcc.Graph(
            id='heatmap'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='linegraph'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(["Zoom level:",
              dcc.Slider(0,
                         3,
                         marks={0: '0%', 3: '100%'},
                         value=0,
                         id='zoom_level')],
             style={'width': '98%', 'padding': '0px 20px 20px 20px','font-family': 'oswald'})
])

