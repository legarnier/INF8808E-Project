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
import vis5
import vis4
import vis2
import vis1
import vis6
import plotly.express as px
from datetime import date
from viz3 import viz_3

from dash.dependencies import Input, Output, State


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])




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


# add your graph title here:

viz1_title = "Current protocol latency in Milliseconds"
viz2_title = "Average Latency per application type"
viz3_title = "Current Latency Geographical Map"
viz4_title = "Average Latency per Site"
viz5_title = "Forecasting Latency"
viz6_title = "Anomaly detection"

viz_titles = [viz1_title, viz2_title, viz3_title,viz4_title, viz5_title, viz6_title]

# Get the vis2
vis2_bubble_df = preprocess.bubble_chart_df(dataframe)
fig2_bubble = vis2.buble_chart(vis2_bubble_df)

fig2_line = vis2.get_empty_figure()


# Get the vis5 dataframe
vis5_df = preprocess.filter_groupby_time_city(dataframe)


app.layout = html.Div(
    [
        dbc.Row(
            [
                # Sidebar
                dbc.Col(
                    [
                        html.Div(
                            children=[
                               html.H1("INF8808 ", className="project-title"),
                                html.H1("Final Project ",
                                        className="project-title"),

                                html.H3("Team Number: 7",
                                        className="team-number"),
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
                                         dbc.Row(
                                        [
                                            dbc.Col(
                                            dbc.Button(
                                            f"Graph {graph_id}",
                                            id='button-' + str(graph_id),
                                            color="primary",
                                            outline=True,
                                            style={"text-align": "center","font-size":"small"},
                                        )
                                            
                                            ,width=3
                                        ),
                                        
                                        dbc.Col(
                                            
                                          dbc.CardBody(
                                            [
                                                html.H5(
                                                    viz_titles[graph_id-1], className="card-title"),
                                            ]
                                        ) ,width=9  
                                        ),
                                        dbc.Col(
                                            dbc.Collapse(
                                            dcc.Graph(
                                                id={"type": "graph", "index": graph_id}),
                                                id={"type": "collapse",
                                                "index": graph_id},
                                            is_open=False,
                                            ),width = 3
                                        ) 
                                            
                                        ],
                                         align='center'
                                        )
                                        
                                          
                                    ]
                                ) 
                                for graph_id in range(1, 7)  # Update the range based on the number of graphs
                            ],
                            className="sidebar-content",

                        ),
                        
                        html.Hr(),
                         
                        
                        
                        html.Div(
                            style={'display': 'flex', 'align-items': 'center'},
                            children=[
                                dcc.Download(id="download-text"),
                                html.H3('Project Description:   '),
                                dbc.Button("Download PDF", id="btn-download",color="secondary",outline=True,
                                           style={'color': 'black', 'margin-left':'10px','font-size':'0.8 rem'}),

                               
                            
                            ]
                        ),

                        html.Hr(),
                        
                        html.Div(
                            style={'display': 'flex', 'align-items': 'center','font-size':'1.75rem'},
                            children=[
                                 html.A('Demo video', href='https://www.youtube.com/', className='youtube-link',
                                        style={'color': 'black'}) # set link color to black)
                            ]
                        ),    
                        
                        
                    ],
                    width=3,
                    style={
                        'position': 'fixed',
                        'top': 0,
                        'height': '100vh',
                        #'width': '22%',
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
                                                        dbc.Button(
                                                            "Graph 1: " + viz1_title, className="graph-title", id="graph-title-1"),
                                                    ]
                                                ),
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
                                                            id="graph-body-1",
                                                            style={'display': 'block'}

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
                                                    'left': '33%',
                                                    'margin-top': 20
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
                                                
                                                dbc.CardHeader(dbc.Button( "Graph 2: " + viz2_title, className="graph-title", id="graph-title-2")),

                                                dbc.CardBody(
                                                  [ 
                                                        ######
                                                        vis2.viz2_layout,
                                                        #######
                                                        
                                                        
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
                                                                
                                                        


                                                    ],
                                                    id="graph-body-2",
                                                   style={'display': 'block'}

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
                                        'left': '33%',
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
                                                dbc.CardHeader(dbc.Button("Graph 3: " + viz3_title, className="graph-title",
                                                               id="graph-title-3")),
                                                dbc.CardBody(
                                                    [
                                                        #####
                                                        viz_3.layout
                                                        #####
                                                    ],
                                                    id="graph-body-3",
                                                    style={'display': 'block'}

                                                )
                                            ],
                                            id="graph-card-3",
                                            color="info",

                                        ),
                                    ],
                                    width=12,
                                    style={
                                        'position': 'relative',
                                        'top': 0,
                                        'left': '33%',
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
                                                dbc.CardHeader(dbc.Button(
                                                    "Graph 4: " + viz4_title, className="graph-title", id="graph-title-4")),

                                                dbc.CardBody(
                                                    [
                                                      #########
                                                      vis4.vis4_layout  ,
                                                      ##########
                                                    ],
                                                    id="graph-body-4",
                                                    style={'display': 'block'}

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
                                        'left': '33%',
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
                                                dbc.CardHeader(dbc.Button(
                                                    "Graph 5: " + viz5_title, className="graph-title", id="graph-title-5")),
                                               
                                                dbc.CardBody(
                                                    [
                                                    #####
                                                     vis5.card_layout,
                                                    #####
                                                    
                                                       
                                                        dcc.Graph(
                                                            id='fig5',
                                                            #figure=fig5,
                                                            style={
                                                                'width': '%100'}
                                                        ),
                                                    ],
                                                    id="graph-body-5",
                                                   style={'display': 'block'}

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
                                        'left': '33%',
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
                                                dbc.CardHeader(dbc.Button(
                                                    "Graph 6: " + viz6_title, className="graph-title", id="graph-title-6")),
                                                dbc.CardBody(
                                                    [
                                                        #####
                                                        vis6.layout
                                                        #####
                                                    ],
                                                    id="graph-body-6",
                                                    style={'display': 'block'}

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
                                        'left': '33%',
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
            style={'font-family': 'oswald'}
        ),
    ]
)

# # Updating the current latencies

@app.callback(
    Output("gauges-container", "children"),
    [
        Input("button-site-qc", "n_clicks"),
        Input("button-site-on", "n_clicks"),
        Input("button-site-man", "n_clicks"),
        Input("radio-type", "value"),
        Input("interval-component", "n_intervals")
    ],
)
def update_gauges(site_qc_clicks, site_on_clicks, site_man_clicks, radio_type_value, n_intervals):
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
                style={"height": "200px", "width": "16.66%", "margin": "0"},
            )
        )

    return gauges



# apply filters on graph 2
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

        date_df = preprocess.filter_date(
            dataframe, start_date_object, end_date_object)
        vis2_df_filtered = preprocess.bubble_chart_df(date_df)
        fig2 = vis2.buble_chart(vis2_df_filtered)
    else:
        start_date_object = date.fromisoformat(start_date)
        end_date_object = date.fromisoformat(end_date)

        date_df = preprocess.filter_date(
            dataframe, start_date_object, end_date_object)
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

    # draw line chart without any filetr
    elif bubble_clicked is not None and start_date is None and protocol == 'All':
        application_type = preprocess.bubble_select(dataframe, date(
            2023, 6, 1), date(2023, 6, 5), protocol, bubble_clicked)
        if application_type == None:
            fig2_line = vis2.get_empty_figure()
        else:
            vis2_line_df = preprocess.line_chart_df(
                dataframe, application_type, date(2023, 6, 1), date(2023, 6, 5))
            fig2_line = vis2.line_chart(vis2_line_df, application_type)

    elif start_date is not None and protocol == 'All':  # draw line chart based on date range filter only
        start_date_object = date.fromisoformat(start_date)
        end_date_object = date.fromisoformat(end_date)
        application_type = preprocess.bubble_select(
            dataframe, start_date_object, end_date_object, protocol, bubble_clicked)
        if application_type == None:
            fig2_line = vis2.get_empty_figure()
        else:
            date_df = preprocess.filter_date(
                dataframe, start_date_object, end_date_object)
            vis2_line_df = preprocess.line_chart_df(
                date_df, application_type, start_date_object, end_date_object)
            fig2_line = vis2.line_chart(vis2_line_df, application_type)

    elif start_date is None and protocol != 'All':  # draw the line chart based on protocol filter only
        application_type = preprocess.bubble_select(dataframe, date(
            2023, 6, 1), date(2023, 6, 5), protocol, bubble_clicked)

        if application_type == None:
            fig2_line = vis2.get_empty_figure()
        else:
            filtered_df = preprocess.filter_protocol(dataframe, protocol)
            vis2_line_df = preprocess.line_chart_df(
                filtered_df, application_type,  date(2023, 6, 1), date(2023, 6, 5))
            fig2_line = vis2.line_chart(vis2_line_df, application_type)

    else:  # draw the line chart based on filters and bubble clicked
        start_date_object = date.fromisoformat(start_date)
        end_date_object = date.fromisoformat(end_date)
        application_type = preprocess.bubble_select(
            dataframe, start_date_object, end_date_object, protocol, bubble_clicked)

        if application_type == None:
            fig2_line = vis2.get_empty_figure()
        else:
            date_df = preprocess.filter_date(
                dataframe, start_date_object, end_date_object)
            filtered_df = preprocess.filter_protocol(date_df, protocol)
            vis2_line_df = preprocess.line_chart_df(
                filtered_df, application_type, start_date_object, end_date_object)
            fig2_line = vis2.line_chart(vis2_line_df, application_type)

    return fig2_line



@app.callback(
    Output("graph-body-1", "style"),
    Input("graph-title-1", "n_clicks"),
    Input("button-1", "n_clicks")
    ,State('graph-body-1', 'style')
)
@app.callback(
    Output("graph-body-2", "style"),
    Input("graph-title-2", "n_clicks"),
    Input("button-2", "n_clicks")
    ,State('graph-body-2', 'style')

)
@app.callback(
    Output("graph-body-3", "style"),
    Input("graph-title-3", "n_clicks"),
    Input("button-3", "n_clicks")
        ,State('graph-body-3', 'style')

)
@app.callback(
    Output("graph-body-4", "style"),
    Input("graph-title-4", "n_clicks"),
    Input("button-4", "n_clicks")
    ,State('graph-body-4', 'style')

)
@app.callback(
    Output("graph-body-5", "style"),
    Input("graph-title-5", "n_clicks"),
    Input("button-5", "n_clicks")
    ,State('graph-body-5', 'style')

)
@app.callback(
    Output("graph-body-6", "style"),
    Input("graph-title-6", "n_clicks"),
    Input("button-6", "n_clicks")
    ,State('graph-body-6', 'style')

)
def toggle_content(open_clicks, close_clicks, style):
    
    if open_clicks is None and close_clicks is None:
        return style  # No button clicks yet, maintain current style
    display = style.get('display', 'block')

    new_style = {'display': 'none'} if display == 'block' else {'display': 'block'}
    return new_style



@app.callback(
    Output('heatmap', 'figure'),
    Input('place', 'value'),
    Input('type', 'value'))
def vis6_update_heatmap(place, typ):

    # Update the heatmap figure
    fig = vis6.update_heatmap(df_dense,
                              place,
                              typ)
    return fig


@app.callback(
    Output('linegraph', 'figure'),
    Input('heatmap', 'clickData'),
    Input('zoom_level', 'value'),
    Input('place', 'value'),
    Input('type', 'value'),
)
def vis6_update_line(clickData, zoom_level, place, typ):

    # Update the line graph
    fig = vis6.update_line(df_dense, clickData, zoom_level, place, typ)
    return fig


# Callback for updating the animation graph and buttons
@app.callback(
    dash.dependencies.Output('animation-graph', 'figure'),
    dash.dependencies.Input('button-dropdown', 'value')
)

def update_graph(button_value):
   
    fig = vis4.update_graph(button_value,dataframe)
    return fig
        

@app.callback(
    Output('fig5', 'figure'),
    Input('viz5_places', 'value')
)
def vis5_update_linechart(viz5_places):

    # Create the line chart figure
    fig = vis5.update_vis5(vis5_df.loc[vis5_df['Site'] == viz5_places], viz5_places)
    return fig

# Callbacks for the download button
@app.callback(
    Output("download-text", "data"),
    Input("btn-download", "n_clicks"),
    prevent_initial_call=True,
)
def func1(n_clicks):
    return dcc.send_file("../data/Project Description.pdf")

if __name__ == "__main__":
    app.run_server(debug=True)
