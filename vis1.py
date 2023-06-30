import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import preprocess
import pandas as pd
import plotly.graph_objs as go



# Get data
dataframe = pd.read_csv('../data/dataset.csv')

# Get the data preprocessed

# The data is a row of  the protocol latencies so we have to reshape it
# to have for each site and each type a row for the latency value of the 
# protocol on target
# So first of all we:
##################### *Filter by sites and by types into dictionnaries
dict_data_site = preprocess.filter_by_Site(dataframe)

Qc_by_type = preprocess.filter_by_type(dict_data_site['Quebec'])
On_by_type = preprocess.filter_by_type(dict_data_site['Ontario'])
Man_by_type = preprocess.filter_by_type(dict_data_site['Manitoba'])


QC_latency_network = Qc_by_type['network']
QC_latency_app = Qc_by_type['app']

ON_latency_network = On_by_type['network']
ON_latency_app = On_by_type['app']

MAN_latency_network = Man_by_type['network']
MAN_latency_app = Man_by_type['app']

############################
## and then we
####### *Transform the new data dictionnary to dataframe to make it easier to display

QC_latency_network_df = preprocess.Protocol_to_df(QC_latency_network)
ON_latency_network_df = preprocess.Protocol_to_df(ON_latency_network)
MAN_latency_network_df = preprocess.Protocol_to_df(MAN_latency_network)


QC_latency_app_df = preprocess.Protocol_to_df(QC_latency_app)
ON_latency_app_df = preprocess.Protocol_to_df(ON_latency_app)
MAN_latency_app_df = preprocess.Protocol_to_df(MAN_latency_app)

Qc_by_type['network'] = QC_latency_network_df
On_by_type['network'] = ON_latency_network_df
Man_by_type['network'] = MAN_latency_network_df

Qc_by_type['app'] = QC_latency_app_df
On_by_type['app'] = ON_latency_app_df
Man_by_type['app'] = MAN_latency_app_df

dict_data_site['Quebec'] = Qc_by_type
dict_data_site['Ontario'] = On_by_type
dict_data_site['Manitoba'] = Man_by_type

#####################
# And then we choose the
######## *Data used for the default display
data = dict_data_site['Quebec']['app']

variables = ['HTTP', 'HTTPS', 'TCP', 'ICMP', 'TWAMP', 'UDP']
num_gauges = len(variables)
default_row_index = 0

#####################

# Then we display a gauge for each protocol latency from each site and type
# Generative function for each gauge
def generate_gauge_figure(value, variable,ref=0):
    return go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=value,
            title={'text': variable},
            delta={'reference': ref,'increasing': {'color': 'red'}, 'decreasing': {'color': 'green'}},
            gauge={
                'axis': {'range': [None, 100]},
                    'bar': {'color': 'rgb(0, 128, 255)'},
                    'bgcolor': 'white',
                    'borderwidth': 2,
                    'bordercolor': 'gray',
                    'steps': [
                        {'range': [0, value], 'color': 'rgb(0, 70, 140)'},
                        {'range': [value, 100], 'color': 'rgb(0, 128, 255)'}
                    ]
                
            }
        ),
        layout=go.Layout(
            margin={"l": 0, "r": 0, "t": 0, "b": 0},
            width=200,
            height=200
        ),
    )
############################

############################ Layout display
layout = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H5("Site "),
                dbc.Button(
                    "Quebec",
                    id="button-site-qc",
                    color="primary",
                    className="mr-1"
                ),
                dbc.Button(
                    "Ontario",
                    id="button-site-on",
                    color="primary",
                    className="mr-1"
                ),
                dbc.Button(
                    "Manitoba",
                    id="button-site-man",
                    color="primary",
                    className="mr-1"
                ),
                html.H5("Protocol Type "),
                dcc.RadioItems(
                    id="radio-type",
                    options=[
                        {"label": " Application ", "value": "app"},
                        {"label": " Network ", "value": "network"}
                    ],
                    value="app",
                    className="mb-2"
                ),
                html.Div(
                    id="gauges-container",
                    style={"display": "flex", "justify-content": "center"}
                ),
                dcc.Interval(
                    id="interval-component",
                    interval=3000,
                    n_intervals=0
                )
            ],
            id="graph-body"
        ),
    ],
    id="graph-card",
    color="info",
)


############################ Update the gauges with the next line
# Given the data is sorted by time, two consecutive row are consecutive latencies
# So the first gauges displayed are actually the first row of the dataset and then we update 
# the data by a frequency chosen considering the delay between two latency values and also
# the perfomance of the server, but for this visualization we chose a 3 seconds frequency
def update_gauges( radio_type_value, n_intervals):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "button-site-qc"

    if button_id == "button-site-qc":
        selected_data = dict_data_site['Quebec'][radio_type_value]
    elif button_id == "button-site-on":
        selected_data = dict_data_site['Ontario'][radio_type_value]
    elif button_id == "button-site-man":
        selected_data = dict_data_site['Manitoba'][radio_type_value]
    else:
        selected_data = dict_data_site['Quebec'][radio_type_value]

    row_index = n_intervals % len(selected_data)
    ref_index = row_index - 1
    gauges = []
    for i, variable in enumerate(variables):
        figure = preprocess.generate_gauge_figure(selected_data.iloc[row_index][variable], variable,selected_data.iloc[ref_index][variable])
        gauges.append(
            dcc.Graph(
                id=f"gauge{i+1}",
                figure=figure,
                config={"displayModeBar": False},
                style={"height": "200px", "width": "200px", "margin": "0"},
            )
        )

    return gauges
