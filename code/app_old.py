import pathlib, dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import preprocess,vis5,viz4
import pandas as pd
import dash_bootstrap_components as dbc



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])



# Get the data
dataframe = pd.read_csv('../data/dataset.csv')



#Get the vis5 
vis5_df = preprocess.filter_groupby_time_city(dataframe)
fig5 = vis5.initial(vis5_df)

fig5.update_layout(height = 700, width = 1800)
fig5.update_layout(autosize=True)


fig4 = vis5.initial(dataframe)
fig4.update_layout(height = 700, width = 1800)
fig4.update_layout(autosize=True)






# Styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


# Padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


# Sidebar content
sidebar = html.Div(
    [
        html.H2("INF8808", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Dashboard", href="/", active="exact"),
                dbc.NavLink("Transformer Performance", href="/page-1", active="exact"),
                dbc.NavLink("Tap changer Performance", href="/page-2", active="exact"),
                dbc.Button(
                            "Visualization 5",
                            id="button-5",
                            n_clicks=0,
                            className="button-style",
                        )
                        
            ],
            vertical=True,
            pills=True,
         ),
            dcc.Graph(
                                    id = 'fig5',
                                    figure = fig5,
                                    style={'width': '%100', 'display': 'inline-block'}
                            )

    ],
    style=SIDEBAR_STYLE,
)



content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
    
])


"""
app.layout = html.Div(
    children=[

        html.H1("Latency Visualization", className="title"),
        html.Div(
            children=[
                html.Div(
                    className="buttons",
                    children=[
                        html.Button(
                            "Visualization 1",
                            id="button-1",
                            n_clicks=0,
                            className="button-style",
                        ),
                        html.Button(
                            "Visualization 2",
                            id="button-2",
                            n_clicks=0,
                            className="button-style",
                        ),
                        html.Button(
                            "Visualization 3",
                            id="button-3",
                            n_clicks=0,
                            className="button-style",
                        ),
                        html.Button(
                            "Visualization 4",
                            id="button-4",
                            n_clicks=0,
                            className="button-style",
                        ),
                        dcc.Graph(
                                id = 'fig4',
                                figure = fig4,
                                style={'width': '%100', 'display': 'inline-block'}
                        ),
                        html.Button(
                            "Visualization 5",
                            id="button-5",
                            n_clicks=0,
                            className="button-style",
                        ),
                        
                        dcc.Graph(
                                id = 'fig5',
                                figure = fig5,
                                style={'width': '%100', 'display': 'inline-block'}
                        ),

                        #html.Label('You can find forecasting visualization here:'),
                        
                    

                        html.Button(
                            "Visualization 6",
                            id="button-6",
                            n_clicks=0,
                            className="button-style",
                        ),
                    ],
                ),
                html.Div(
                    className="plot",
                    children=[
                        html.H1(id="plot-text", children=""),
                    ],
                )], style={"display": "flex",'width': '100%'}),
    ],
)
"""




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
    Output('fig4', 'style'),
    [Input('button-4', 'n_clicks')]
)   
def toggle_graph_visibility(n_clicks):
    if n_clicks and n_clicks % 2 == 1:
        return {'display': 'none'}  # Hide the graph
    else:
        return {'display': 'block'}  # Show the graph  

@app.callback(
    Output("plot-text", "children"),
    Input("button-1", "n_clicks"),
    Input("button-2", "n_clicks"),
    Input("button-3", "n_clicks"),
    Input("button-4", "n_clicks"),
    Input("button-5", "n_clicks"),
    Input("button-6", "n_clicks"),
)
def update_plot(n_clicks):
    button_texts = [
        "Visualization 1",
        "Visualization 2",
        "Visualization 3",
        "Visualization 4",
        "Visualization 5",
        "Visualization 6",
    ]
    triggered_button_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if triggered_button_id:
       button_index = int(triggered_button_id.split("-")[1]) - 1
       return button_texts[button_index]
    
    return None
