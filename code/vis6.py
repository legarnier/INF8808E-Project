from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd



df = pd.read_csv(('../data/dense_dataset.csv'))

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


layout = html.Div([
    html.Div([
        # BEGIN LEFT PART
        html.Div([
            dcc.Dropdown(
                [{"label": html.Span("Quebec",
                                     style={'color': 'red'}),
                  "value": "Quebec"},
                 {"label": html.Span("Ontario",
                                     style={'color': 'blue'}),
                  "value": "Ontario"},
                 {"label": html.Span("Manitoba",
                                     style={'color': 'green'}),
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
            style={'width': '49%', 'display': 'inline-block'}),
        # END LEFT PART

        # BEGIN RIGHT PART
        html.Div(["GRAPH"], style={'width': '49%',
                 'float': 'right', 'display': 'inline-block'})
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

    html.Div("zoom level:")
])




if __name__ == '__main__':
    app.run_server(debug=True)
