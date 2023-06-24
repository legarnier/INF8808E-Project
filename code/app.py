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
import vis5,vis4
from dash.dependencies import Input, Output
#viz_3
import json
import plotly.graph_objects as go
from viz3 import map_viz
from viz3 import helper

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# Get the data
dataframe = pd.read_csv('../data/dataset.csv')

#Get the vis5 
vis5_df = preprocess.filter_groupby_time_city(dataframe)
fig5 = vis5.initial(vis5_df)

fig5.update_layout(height = 700, width = 1300)
fig5.update_layout(autosize=True)



#Get the vis4

fig4 = vis4.animated_line(dataframe)

fig4.update_layout(height = 700, width = 1300)
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
                            'width': '23%',
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
                                                dbc.CardHeader(dbc.Button("Graph 1: " + viz1_title, className="graph-title",id="graph-title-1")),
                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            figure={"data": [{"y": [1, 3, 2, 4]}]},
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
                                        'left': '30%'
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
                                                dbc.CardHeader(dbc.Button("Graph 2: " + viz2_title, className="graph-title",id="graph-title-2")),

                                                dbc.CardBody(
                                                    [
                                                        dcc.Graph(
                                                            figure={"data": [{"y": [1, 3, 2, 4]}]},
                                                            id='fig2'
                                                        ),
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
                                        'top': 20,
                                        'left': '30%'
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
                                                html.H4("Graph 3", className="graph-title"),
                                                dcc.Graph(
                                                    figure={"data": [{"y": [3, 1, 4, 2]}]},
                                                    id='fig3'
                                                ),
                                            ],
                                            id="graph-alert-3",
                                            color="info",
                                        ),
                                    ],
                                    width=12,
                                    style={
                                        'position': 'relative',
                                        'top': 40,
                                        'left': '30%'
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
                                        'top': 60,
                                        'left': '30%'
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
                                        'top': 80,
                                        'left': '30%'
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
                                                        dcc.Graph(
                                                            figure={"data": [{"y": [1, 3, 2, 4]}]},
                                                            id='fig6'
                                                        ),
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
                                        'top': 100,
                                        'left': '30%'
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
    Input("graph-title-5", "n_clicks")
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
    


if __name__ == "__main__":
    app.run_server(debug=True)
