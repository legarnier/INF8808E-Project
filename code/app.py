import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import preprocess
import vis5,vis4, vis2, vis1
import vis6
import plotly.express as px
from datetime import date


from dash.dependencies import Input, Output
#viz_3
import json
import plotly.graph_objects as go
from viz3 import map_viz
from viz3 import helper

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# Get the data
dataframe = pd.read_csv('../data/dataset.csv')
df_dense = pd.read_csv(('../data/dense_dataset.csv'))


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

variables = MAN_latency_app['Protocol'].unique()
df_values = MAN_latency_app[MAN_latency_app['Time'] == MAN_latency_app['Time'].unique()[0]]
values = df_values['Latency'].tolist()
gauges = vis1.gauge_chart(variables,values)


# viz_3
with open('../data/georef-canada-province@public.geojson', encoding='utf-8') as data_file:
    map_data = json.load(data_file)
locations = preprocess.get_neighborhoods(map_data)
z = len(map_data['features']) * [1]
fig = go.Figure()
fig = map_viz.add_choro_trace(fig, map_data, locations, z)
fig = map_viz.add_scatter_traces(fig, dataframe)

fig = helper.adjust_map_style(fig)
fig = helper.adjust_map_sizing(fig)
fig = helper.adjust_map_info(fig)
fig.update_layout(height = 700, width = 1000)

#add your graph title here: 

viz1_title = "Current protocol latency"
viz2_title = "Average Latency per application type"
viz3_title = "viz3_title"
viz4_title = "viz4_title"
viz5_title = "Forecasting Latency"
viz6_title = "viz6_title"

viz_titles = [viz1_title,viz2_title,viz3_title,viz4_title,viz5_title,viz6_title]

#Get the vis2
vis2_bubble_df = preprocess.bubble_chart_df(dataframe)
fig2_bubble = vis2.buble_chart(vis2_bubble_df)

fig2_line = vis2.get_empty_figure()


#Get the vis5 
vis5_df = preprocess.filter_groupby_time_city(dataframe)
fig5 = vis5.initial(vis5_df)

fig5.update_layout(height = 700, width = 1300)
fig5.update_layout(autosize=True)



#Get the vis4

fig4 = vis4.animated_line(dataframe)

fig4.update_layout(height = 700, width = 1500)
fig4.update_layout(autosize=True)


app.layout = html.Div(
    [
        dbc.Row(
            [
                # Sidebar
                dbc.Col(
                    [
                        html.Div(
                            children=
                            [
                                html.H1("INF8808 ", className="project-title"),
                               html.H1("Final Project ", className="project-title"),

                                html.H3("Team Number: 7", className="team-number"),
                                html.H3("Summer 2023", className="date"),
                            ],
                            className="header-container",

                            style={
                                
                                'backgroundColor': '#B0E2FF'
                                
                              },
                        ),
                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem(
                                    [
                                        dbc.Button(
                                            f"Graph {graph_id}",
                                            id='button-' + str(graph_id),
                                            color="primary",
                                            outline=True,
                                            style={"text-align": "left","margin-bottom":20},
                                        ),
                                          dbc.CardBody(
                                            [
                                                html.H4(viz_titles[graph_id-1], className="card-title"),
                                            ]
                                        ),
                                        dbc.Collapse(
                                            dcc.Graph(id={"type": "graph", "index": graph_id}),
                                            id={"type": "collapse", "index": graph_id},
                                            is_open=False,
                                        ),
                                    ]
                                )   
                                
                                for graph_id in range(1, 7)  # Update the range based on the number of graphs
                            ],
                            className="sidebar-content",

                        ),
                        
                        
                    ],
                    width=3,
                    style={
                            'position': 'fixed',
                            'top': 0,
                            'height': '100vh',
                            'width': '22%',
                             'backgroundColor': '#B0E2FF'
                        },
                    className="sidebar",
                    
                ),
                # Graphs
                dbc.Col(
                    [
                        
                        
                         dbc.Row(
                            [
                                dbc.Col(
                                        [
                                            dbc.Card(
                                                [
                                                    dbc.CardHeader(
                                                        [
                                                            dbc.Button("Graph 1: " + viz1_title, className="graph-title", id="graph-title-1"),
                                                        ]
                                                    ),
                                                    dbc.CardBody(
                                                        [
                                                            html.H5("Site :"),
                                                            dbc.Button("Quebec", id="button-site-qc", color="primary", className="mr-1"),
                                                            dbc.Button("Ontario", id="button-site-on", color="primary", className="mr-1"),
                                                            dbc.Button("Manitoba", id="button-site-man", color="primary", className="mr-1"),
                                                            dcc.RadioItems(
                                                                id="radio-type",
                                                                options=[
                                                                    {"label": "Protocol type Application", "value": "app"},
                                                                    {"label": "Protocol type Network", "value": "network"}
                                                                ],
                                                                value="app",
                                                                className="mb-2"
                                                            ),
                                                            dcc.Graph(
                                                                figure=gauges,
                                                                id='fig1'
                                                            ),
                                                        ],
                                                        id="graph-body-1"
                                                    ),
                                                ],
                                                id="graph-card-1",
                                                color="info",
                                                    ),
                                                ],
                                                width=12,
                                                style={
                                                    'position': 'relative',
                                                    'top': 0,
                                                    'left': '30%',
                                                    'margin-top': 20
                                                },
                                            )
                                    ,
                            ]
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(dbc.Button("Graph 2: " + viz2_title, className="graph-title",id="graph-title-2")),
                                                dbc.CardBody(
                                                    [
                                                        html.Div(className='vis2-container', style={'display': 'flex'} ,children=[
                                                            dcc.Graph(
                                                                    id = 'fig2-bubble',
                                                                    className = 'vis2-graph',
                                                                    figure = fig2_bubble,
                                                                    style={'display': 'inline', 'width': '60%'}
                                                                ),
                                                            dcc.Graph(
                                                                    id = 'fig2-line',
                                                                    className = 'vis2-graph',
                                                                    figure = fig2_line,
                                                                    style={'display': 'inline', 'width': '40%'}
                                                                ),
                                                            ]),
                                                            html.Div(className = 'filter-container', children=[
                                                            html.Label('Date range', style={'padding-top': '2%', 'padding-left': '2%'}),
                                                            html.Div([
                                                                dcc.DatePickerRange(
                                                                        id='filter_date',
                                                                        start_date_placeholder_text="Start Period",
                                                                        end_date_placeholder_text="End Period",
                                                                        calendar_orientation='vertical',
                                                                        min_date_allowed=date(2023, 6, 1),
                                                                        max_date_allowed=date(2023, 6, 5),
                                                                        initial_visible_month=date(2023, 6, 5),
                                                                        end_date=date(2023, 6, 5),
                                                                        style={'padding': '2%'}
                                                                    ), 
                                                                    html.Div(id='output-container-date-picker-range')
                                                                ]),
                                                                html.Label('Protocol', style={'padding-top': '2%', 'padding-left': '2%'}),
                                                                html.Div([
                                                                    dcc.Dropdown(['All', 'HTTP','HTTPS', 'TCP', 'UDP', 'ICMP', 'TWAMP'], 'All', id='filter_protocol', style={'width': '100px'}),
                                                                    html.Div(id='output'),     
                                                                ], style={'padding': '2%', 'display': 'inline-flex'}),
                                                            ]),
                                                    ],
                                                    id="graph-body-2"
                                                ),
                                            ],
                                            id="graph-card-2",
                                            color="info",
                                        ),
                                    ],
                                    width=12,
                                    style={
                                        'position': 'relative',
                                        'top': 0,
                                        'left': '30%',
                                          'margin-top' : 20

                                    },
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Alert(
                                            [
                                                html.H4("Graph 3", className="graph-title"),
                                                html.Div(
                                                    style={
                                                        'display':'flex'
                                                    },
                                                    children=[
                                                    dcc.Graph(figure=fig, id='graph',
                                                              config=dict(
                                                                  showTips=False,
                                                                  showAxisDragHandles=False,
                                                                  displayModeBar=False)),

                                                    html.Div(
                                                        style={
                                                            'width': '100px',
                                                            'margin-top': '120px'
                                                        },
                                                        className='panel-div',
                                                        children=[
                                                            html.P('Letancy',
                                                                   style={
                                                                       'font-family': 'Oswald',
                                                                       'font-size': '28'
                                                                   }),
                                                            html.Div(id='panel', style={
                                                                'border': '1px solid black',
                                                                'width': '100px',
                                                                'padding': '3px',
                                                                'display': 'flex',
                                                                'flex-direction': 'column',
                                                                'align-items': 'center'
                                                            },
                                                                     children=[
                                                                         html.Div(
                                                                             style={
                                                                                 'display': 'flex',
                                                                                 'flex-direction': 'row'
                                                                             },
                                                                             children=[
                                                                                 html.Div(
                                                                                     style={
                                                                                            'height': '10.52px',
                                                                                            'width': '10.52px',
                                                                                            'background-color': 'transparent',
                                                                                            'border-radius': '50%',
                                                                                            'display': 'inline-block',
                                                                                            'border': '1px solid black',
                                                                                            'margin':'2px'
                                                                                     }
                                                                                 ),
                                                                                 html.P('21.04 ms',
                                                                                        style={
                                                                                            'margin': '0px',
                                                                                            'font-size': '.6rem',
                                                                                            'padding-left': '8px'
                                                                                        })]
                                                                         ),
                                                                         html.Div(
                                                                             style={
                                                                                 'margin-right': '42px',
                                                                                 'height': '23.32px',
                                                                                 'width': '23.32px',
                                                                                 'background-color': 'transparent',
                                                                                 'border-radius': '50%',
                                                                                 'display': 'inline-block',
                                                                                 'border': '1px solid black',
                                                                             }  
                                                                         ),
                                                                         html.Div(
                                                                             style={
                                                                                'margin':'2px 42px 2px 0',
                                                                                'height': '36.14px',
                                                                                'width': '36.14px',
                                                                                'background-color': 'transparent',
                                                                                'border-radius': '50%',
                                                                                'display': 'inline-block',
                                                                                'border': '1px solid black',
                                                                             }),
                                                                         html.Div(
                                                                             style={
                                                                                 'display': 'flex',
                                                                                 'flex-direction': 'row'
                                                                             },
                                                                             children=[
                                                                                 html.Div(
                                                                                    style={
                                                                                         'height': '48.94px',
                                                                                         'width': '48.94px',
                                                                                         'background-color': 'transparent',
                                                                                         'border-radius': '50%',
                                                                                         'display': 'inline-block',
                                                                                         'border': '1px solid black',
                                                                                     }
                                                                                 ),
                                                                                 html.P('97.88 ms',
                                                                                        style={
                                                                                            'margin-top': '20px',
                                                                                            'font-size': '0.6rem',
                                                                                            'padding-left': '8px'
                                                                                        })]),
                                                                     ])]
                                                    )]
                                                )
                                            ],
                                            id="graph-alert-3",
                                            color="info",
                                            dismissable=True,
                                        ),
                                    ],
                                    width=12,
                                    style={
                                        'position': 'relative',
                                        'top': 0,
                                        'left': '30%',
                                        'margin-top' : 20

                                    },
                                ),
                            ]
                        ),
                        
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                         dbc.Card(
                                            [
                                                dbc.CardHeader(dbc.Button("Graph 3: " + viz3_title, className="graph-title",id="graph-title-3")),

                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            figure={"data": [{"y": [1, 3, 2, 4]}]},
                                                            id='fig3'
                                                        ),
                                                    ],
                                                    id="graph-body-3"
                                                ),
                                            ],
                                            id="graph-card-3",
                                            color="info",
                                        ),
                                    ],
                                    width=12,
                                    style={
                                        'position': 'relative',
                                        'top': 0,
                                        'left': '30%',
                                      'margin-top' : 20

                                    },
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                         dbc.Card(
                                            [
                                                dbc.CardHeader(dbc.Button("Graph 4: " + viz4_title, className="graph-title",id="graph-title-4")),
                                               
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            id = 'fig',
                                                            figure = fig4,
                                                            style={'width': '%100', 'display': 'inline-block'}
                                                        ),
                                                    ],
                                                    id="graph-body-4"
                                                ),
                                            ],
                                            id="graph-card-4",
                                            color="info",
                                        ),
                                    ],
                                    width=12,
                                    style={
                                        'position': 'relative',
                                        'top': 0,
                                        'left': '30%',
                                        'margin-top' : 20

                                    },
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                         dbc.Card(
                                            [
                                                dbc.CardHeader(dbc.Button("Graph 5: " + viz5_title, className="graph-title",id="graph-title-5")),
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            id = 'fig5',
                                                            figure = fig5,
                                                            style={'width': '%100', 'display': 'inline-block'}
                                                        ),
                                                    ],
                                                    id="graph-body-5"
                                                ),
                                            ],
                                            id="graph-card-5",
                                            color="info",
                                        ),
                                    ],
                                    width=12,
                                    style={
                                        'position': 'relative',
                                        'top': 0,
                                        'left': '30%',
                                        'margin-top' : 20

                                    },
                                ),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                          dbc.Card(
                                            [
                                                dbc.CardHeader(dbc.Button("Graph 6: " + viz6_title, className="graph-title",id="graph-title-6")),
                                                dbc.CardBody(
                                                    [
                                                        #####
                                                        vis6.layout
                                                        #####
                                                    ],
                                                    id="graph-body-6"
                                                ),
                                            ],
                                            id="graph-card-6",
                                            color="info",
                                        ),
                                    ],
                                    width=12,
                                    style={
                                        'position': 'relative',
                                        'top': 0,
                                        'left': '30%',
                                        'margin-top' : 20

                                    },
                                ),
                            ]
                        ),
                    ],
                    width=9,
                    className="graph-area",
                ),
            ],
            className="main-row",
        ),
    ]
)

# # Updating the current latencies
# @app.callback(
#     Output('fig1', 'figure'),
#     Input('button-site-qc', 'n_clicks'),
#     Input('button-site-on', 'n_clicks'),
#     Input('button-site-man', 'n_clicks'),
#     Input('source-type', 'value')
# )
# def update_gauges(source1_clicks, source2_clicks, source3_clicks, type_value):
#     # check selected source
#     if source1_clicks:
#         # site 1 sélectionnée
#         source = "Source 1"
#     elif source2_clicks:
#         # Source 2 sélectionnée
#         source = "Source 2"
#     elif source3_clicks:
#         # Source 3 sélectionnée
#         source = "Source 3"
#     else:
#         # Par défaut, utilisez la Source 1
#         source = "Source 1"

#     # Déterminez le type sélectionné
#     if type1_value == "type1":
#         # Type 1 sélectionné
#         type_value = "Type 1"
#     else:
#         # Type


#apply filters on graph 2
@app.callback(
        Output('fig2-bubble', 'figure'), 
        [Input('filter_date', 'start_date'),
        Input('filter_date', 'end_date'),
        Input('filter_protocol', 'value')]
        )
def update_output(start_date, end_date, value):
    dataframe = pd.read_csv('../data/dataset.csv') 
    if value == 'All' and start_date is None:
        fig2 = vis2.buble_chart(vis2_bubble_df)
    elif value != 'All' and start_date is None:
        protocol_df = preprocess.filter_protocol(dataframe, value)
        vis2_df_filtered = preprocess.bubble_chart_df(protocol_df)
        fig2 = vis2.buble_chart(vis2_df_filtered)
    elif value == 'All' and start_date is not None and end_date is not None:
        start_date_object = date.fromisoformat(start_date)
        end_date_object = date.fromisoformat(end_date)

        date_df = preprocess.filter_date(dataframe, start_date_object, end_date_object)
        vis2_df_filtered = preprocess.bubble_chart_df(date_df)
        fig2 = vis2.buble_chart(vis2_df_filtered)
    else:
        start_date_object = date.fromisoformat(start_date)
        end_date_object = date.fromisoformat(end_date)

        date_df = preprocess.filter_date(dataframe, start_date_object, end_date_object)
        filtered_df = preprocess.filter_protocol(date_df, value)
        vis2_df_filtered = preprocess.bubble_chart_df(filtered_df)
        fig2 = vis2.buble_chart(vis2_df_filtered)

    return fig2

# Graph2: change line chart based in the clicked point on bubble chart
@app.callback(
    Output('fig2-line', 'figure'),
    [Input('fig2-bubble', 'clickData'),
    Input('filter_date', 'start_date'),
    Input('filter_date', 'end_date'),
    Input('filter_protocol', 'value')]
)
def bubble_clicked(bubble_clicked, start_date, end_date, protocol): 
    dataframe = pd.read_csv('../data/dataset.csv')
    if bubble_clicked is None:
        fig2_line = vis2.get_empty_figure()

    elif bubble_clicked is not None and start_date is None and protocol == 'All': #draw line chart without any filetr
        application_type = preprocess.bubble_select(dataframe, date(2023, 6, 1), date(2023, 6, 5), protocol, bubble_clicked)
        if application_type == None:
            fig2_line = vis2.get_empty_figure()
        else:
            vis2_line_df = preprocess.line_chart_df(dataframe, application_type, date(2023, 6, 1), date(2023, 6, 5))
            fig2_line = vis2.line_chart(vis2_line_df, application_type)

    elif start_date is not None and protocol == 'All': # draw line chart based on date range filter only
        start_date_object = date.fromisoformat(start_date)
        end_date_object = date.fromisoformat(end_date)
        application_type = preprocess.bubble_select(dataframe, start_date_object, end_date_object, protocol, bubble_clicked)
        if application_type == None:
            fig2_line = vis2.get_empty_figure()
        else:
            date_df = preprocess.filter_date(dataframe, start_date_object, end_date_object)
            vis2_line_df = preprocess.line_chart_df(date_df, application_type, start_date_object, end_date_object)
            fig2_line = vis2.line_chart(vis2_line_df, application_type)

    elif start_date is None and protocol != 'All': #draw the line chart based on protocol filter only
        application_type = preprocess.bubble_select(dataframe, date(2023, 6, 1), date(2023, 6, 5), protocol, bubble_clicked)

        if application_type == None:
            fig2_line = vis2.get_empty_figure()
        else:
            filtered_df = preprocess.filter_protocol(dataframe, protocol)
            vis2_line_df = preprocess.line_chart_df(filtered_df, application_type,  date(2023, 6, 1), date(2023, 6, 5))
            fig2_line = vis2.line_chart(vis2_line_df, application_type)

    else: #draw the line chart based on filters and bubble clicked
        start_date_object = date.fromisoformat(start_date)
        end_date_object = date.fromisoformat(end_date)
        application_type = preprocess.bubble_select(dataframe, start_date_object, end_date_object, protocol, bubble_clicked)

        if application_type == None:
            fig2_line = vis2.get_empty_figure()
        else:
            date_df = preprocess.filter_date(dataframe, start_date_object, end_date_object)
            filtered_df = preprocess.filter_protocol(date_df, protocol)
            vis2_line_df = preprocess.line_chart_df(filtered_df, application_type, start_date_object, end_date_object)
            fig2_line = vis2.line_chart(vis2_line_df, application_type)
    

    return fig2_line

@app.callback(
    Output('fig1', 'style'),
    [Input('button-1', 'n_clicks')]
)

@app.callback(
    Output('fig2', 'style'),
    [Input('button-2', 'n_clicks')]
)

@app.callback(
    Output('fig3', 'style'),
    [Input('button-3', 'n_clicks')]
)
@app.callback(
    Output('fig4', 'style'),
    [Input('button-4', 'n_clicks')]
)

@app.callback(
    Output('fig5', 'style'),
    [Input('button-5', 'n_clicks')]
)
@app.callback(
    Output('fig6', 'style'),
    [Input('button-6', 'n_clicks')]
)
def toggle_graph_visibility(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'display': 'none'}  # Hide the graph
    else:
        return {'display': 'block'}  # Show the graph


@app.callback(
    Output("graph-body-1", "style"),
    Input("graph-title-1", "n_clicks")
)
@app.callback(
    Output("graph-body-2", "style"),
    Input("graph-title-2", "n_clicks")
)
@app.callback(
    Output("graph-body-3", "style"),
    Input("graph-title-3", "n_clicks")
)
@app.callback(
    Output("graph-body-4", "style"),
    Input("graph-title-4", "n_clicks")
)
@app.callback(
    Output("graph-body-5", "style"),
    Input("graph-title-5", "n_clicks")
)
@app.callback(
    Output("graph-body-6", "style"),
    Input("graph-title-6", "n_clicks")
)
def toggle_graph(n_clicks):
    if n_clicks and n_clicks % 2 == 1:  # Hide graph on odd clicks
        return {"display": "none"}
    else:  # Show graph on even clicks (or before any clicks)
        return {'display': 'block'}  # Show the graph
    


@app.callback(
    Output('heatmap', 'figure'),
    Input('place', 'value'),
    Input('type', 'value'))
def update_graph(place_name, type_name):

    # Create the heatmap figure
    fig = px.imshow(vis6.extract_heatmap_data(df_dense,
                                         place_name,
                                         type_name).T,
                    color_continuous_scale='Reds',
                    origin='lower',
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

    # fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig



@app.callback(
    Output('linegraph', 'figure'),
    Input('heatmap', 'hoverData'),
    Input('place', 'value'),
    Input('type', 'value')
    )
def update_line_graph(hoverData,place_name,type_name,protocol_name='HTTP'):
    protocol_name = 'HTTP'
    if hoverData is not None:
        protocol_name = hoverData['points'][0]['y']
    dataline = df_dense.loc[(df_dense['Site']==place_name)&
                   (df_dense['Type']==type_name)&
                   (df_dense['Protocol']==protocol_name)]
    fig = px.line(dataline,x='Time',y='Latency',
                  title=protocol_name)
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
