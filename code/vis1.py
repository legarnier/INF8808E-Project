import pandas as pd
import preprocess
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

# Get the data
dataframe = pd.read_csv('../data/dataset.csv')
df_dense = pd.read_csv(('../data/dense_dataset.csv'))
df_dense['Time'] = pd.to_datetime(df_dense['Time'])

# Get the vis1
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

data = dict_data_site['Quebec']['app']

# Variables pour les jauges et les boutons radio
variables = ['HTTP', 'HTTPS', 'TCP', 'ICMP', 'TWAMP', 'UDP']
num_gauges = len(variables)
default_row_index = 0

layout =html.Div(
    children=[
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
    ]
)
