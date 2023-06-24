import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import dcc, html
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc
import preprocess,vis5,viz4

from dash.dependencies import Input, Output

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get the data
dataframe = pd.read_csv('../data/dataset.csv')

#Get the vis5 
vis5_df = preprocess.filter_groupby_time_city(dataframe)
fig5 = vis5.initial(vis5_df)

fig5.update_layout(height = 700, width = 1300)
fig5.update_layout(autosize=True)




app.layout = dbc.Container(
    [
        
         dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H1("INF8808 Final project", className="project-title"),
                                html.H3("Team Number: 7", className="team-number"),
                                html.H3("Summer 2023", className="date"),
                            ],
                            className="header-container",
                        ),
                    ],
                    width=12,  # Set width to 12 to take up the full row
                ),
            ]
        ),
        dbc.Row(
            [
                # Left sidebar
                dbc.Col(
                    [
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
                            ]
                        ),
                    ],
                    width=3,
                ),
            ]
        ),
        dbc.Row(
            [
                # Graph area 1
                dbc.Col(
                    [
                        dbc.Alert(
                            "Graph 1 Content",
                            id="graph-alert-1",
                            color="info",
                            dismissable=True,
                        ),
                    ],
                    width=12,  # Set width to 12 to take up the full row
                ),
            ]
        ),
        dbc.Row(
            [
                # Graph area 2
                dbc.Col(
                    [
                        dbc.Alert(
                            "Graph 2 Content",
                            id="graph-alert-2",
                            color="info",
                            dismissable=True,
                        ),
                    ],
                    width=12,  # Set width to 12 to take up the full row
                ),
            ]
        ),
        dbc.Row(
            [
                # Graph area 3
                dbc.Col(
                    [
                        dbc.Alert(
                            "Graph 3 Content",
                            id="graph-alert-3",
                            color="info",
                            dismissable=True,
                        ),
                    ],
                    width=12,  # Set width to 12 to take up the full row
                ),
            ]
        ),
        dbc.Row(
            [
                # Graph area 4
                dbc.Col(
                    [
                        dbc.Alert(
                            "Graph 4 Content",
                            id="graph-alert-4",
                            color="info",
                            dismissable=True,
                        ),
                    ],
                    width=12,  # Set width to 12 to take up the full row
                ),
            ]
        ),
        dbc.Row(
            [
                # Graph area 5
                dbc.Col(
                    [
                        dbc.Alert(
                            "Graph 5 - Forecasting Latency :",
                            id="graph-alert-5",
                            color="info",
                            dismissable=True,
                        ),
                        dcc.Graph(
                                    id = 'fig5',
                                    figure = fig5,
                                    style={'width': '%100', 'display': 'inline-block'}
                            )
                    ],
                    width=12,  # Set width to 12 to take up the full row
                ),
            ]
        ),
        dbc.Row(
            [
                # Graph area 6
                dbc.Col(
                    [
                        dbc.Alert(
                            "Graph 6 Content",
                            id="graph-alert-6",
                            color="info",
                            dismissable=True,
                        ),
                    ],
                    width=12,  # Set width to 12 to take up the full row
                ),
            ]
        ),
    ],
    fluid=False,
    style={"max-width": "1200px", "margin": "0 auto"},
)



@app.callback(
    Output('fig5', 'style'),
    [Input('button-5', 'n_clicks')]
)
def toggle_graph_visibility(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'display': 'none'}  # Hide the graph
    else:
        return {'display': 'block'}  # Show the graph
    
    
if __name__ == "__main__":
    app.run_server(debug=True)
