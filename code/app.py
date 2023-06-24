import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
# import preprocess
import vis5,viz4
from dash.dependencies import Input, Output


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


# Get the data
dataframe = pd.read_csv('../data/dataset.csv')

#Get the vis5 
# vis5_df = preprocess.filter_groupby_time_city(dataframe)
# fig5 = vis5.initial(vis5_df)

fig5.update_layout(height = 700, width = 1300)
fig5.update_layout(autosize=True)


app.layout = html.Div(
    [
        dbc.Row(
            [
                # Sidebar
                dbc.Col(
                    [
                        html.H4("Graphs", className="sidebar-title",style={'position': 'fixed', 'width': '20%', 'height': '100vh'}),
                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem(
                                    [
                                        dbc.Button(
                                            f"Graph {graph_id}",
                                            id='button-' + str(graph_id),
                                            color="primary",
                                            outline=True,
                                            style={"text-align": "left"},
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
                            'width': '20%'
                        },
                    className="sidebar",
                    
                ),
                # Graphs
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H1("INF8808 Final project", className="project-title"),
                                html.H3("Team Number: 7", className="team-number"),
                                html.H3("Summer 2023", className="date"),
                            ],
                            className="header-container",
                            style={
                                'position': 'relative',
                                'top': 0,
                                'left': '30%'
                              },
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Alert(
                                            [
                                                html.H4("Graph 1", className="graph-title"),
                                                dcc.Graph(
                                                    figure={"data": [{"y": [4, 2, 3, 1]}]},
                                                    id='fig1'
                                                ),
                                            ],
                                            id="graph-alert-1",
                                            color="info",
                                            dismissable=True,
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
                                        dbc.Alert(
                                            [
                                                html.H4("Graph 2", className="graph-title"),
                                                dcc.Graph(
                                                    figure={"data": [{"y": [1, 3, 2, 4]}]},
                                                    id='fig2'
                                                ),
                                            ],
                                            id="graph-alert-2",
                                            color="info",
                                            dismissable=True,
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
                                        dbc.Alert(
                                            [
                                                html.H4("Graph 3", className="graph-title"),
                                                dcc.Graph(
                                                    figure={"data": [{"y": [3, 1, 4, 2]}]},
                                                    id='fig3'
                                                ),
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
                                        'left': '30%'
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
                                                html.H4("Graph 4", className="graph-title"),
                                                dcc.Graph(
                                                    figure={"data": [{"y": [2, 4, 1, 3]}]},
                                                    id='fig4'
                                                ),
                                            ],
                                            id="graph-alert-4",
                                            color="info",
                                            dismissable=True,
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
                                        dbc.Alert(
                                            [
                                                html.H4("Graph 5", className="graph-title"),
                                                 dcc.Graph(
                                                        id = 'fig5',
                                                        figure = fig5,
                                                        style={'width': '%100', 'display': 'inline-block'}
                                                )
                                                
                                            ],
                                            id="graph-alert-5",
                                            color="info",
                                            dismissable=True,
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
                                        dbc.Alert(
                                            [
                                                html.H4("Graph 6", className="graph-title"),
                                                dcc.Graph(
                                                    figure={"data": [{"y": [1, 2, 4, 3]}]},
                                                    id = 'fig6',

                                                ),
                                            ],
                                            id="graph-alert-6",
                                            color="info",
                                            dismissable=True,
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
def toggle_graph_visibility(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'display': 'none'}  # Hide the graph
    else:
        return {'display': 'block'}  # Show the graph

@app.callback(
    Output('fig2', 'style'),
    [Input('button-2', 'n_clicks')]
)
def toggle_graph_visibility(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'display': 'none'}  # Hide the graph
    else:
        return {'display': 'block'}  # Show the graph
@app.callback(
    Output('fig3', 'style'),
    [Input('button-3', 'n_clicks')]
)
def toggle_graph_visibility(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'display': 'none'}  # Hide the graph
    else:
        return {'display': 'block'}  # Show the grap
@app.callback(
    Output('fig4', 'style'),
    [Input('button-4', 'n_clicks')]
)
def toggle_graph_visibility(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'display': 'none'}  # Hide the graph
    else:
        return {'display': 'block'}  # Show the graph

@app.callback(
    Output('fig5', 'style'),
    [Input('button-5', 'n_clicks')]
)
def toggle_graph_visibility(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'display': 'none'}  # Hide the graph
    else:
        return {'display': 'block'}  # Show the graph
@app.callback(
    Output('fig6', 'style'),
    [Input('button-6', 'n_clicks')]
)
def toggle_graph_visibility(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'display': 'none'}  # Hide the graph
    else:
        return {'display': 'block'}  # Show the graph



if __name__ == "__main__":
    app.run_server(debug=True)
