import dash
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
from datetime import date
from viz3 import viz_3
from dash.dependencies import Input, Output, State
from callbacks import register_callbacks


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get the data
dataframe = pd.read_csv('../data/dataset.csv')

# graph title:
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
                                      html.Img(src=app.get_asset_url('poly.png')
                                              ,style = {'width':'100%'}   
                                    ),
                                   html.H2("INF8808 - Final Project", className="project-title"
                                            ,style = {'margin-top':'25px'}),               
    
                                    html.H3("Team Number: 7",
                                            className="team-number"),
                                    html.H3("Summer 2023", className="date"),
                                ],
                                className="header-container",
                                style={
                                    'margin-left': '20px',
                                    'margin-top':'25px',
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
                            style={'display': 'flex', 'align-items': 'center','margin-left':'20px'},
                            children=[
                                dcc.Download(id="download-text"),
                                html.H3('Project Description:   '),
                                dbc.Button("Download PDF", id="btn-download",color="secondary",outline=True,
                                           style={'color': 'black', 'margin-left':'10px','font-size':'0.8 rem'}),
                            ]
                        ),

                        html.Hr(),
                        
                        html.Div(
                            style={'display': 'flex', 'align-items': 'center','font-size':'1.75rem','margin-left':'20px'},
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
                        'backgroundColor': '#d3e1f2'
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
                                                            "Graph 1: " + viz1_title, className="graph-title", id="graph-title-1"
                                                            ,style={'background':'#779ecb','font-weight':'bold'}
                                                        ),
                                                    ]
                                                ),
                                                dbc.CardBody(
                                                            [
                                                               #####
                                                                vis1.layout
                                                               #####
                                                            ],
                                                            id="graph-body-1",
                                                            style={'display': 'block','background':'#779ecb'}
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
                                                dbc.CardHeader(dbc.Button( "Graph 2: " + viz2_title, className="graph-title", id="graph-title-2"
                                                                          ,style={'background':'#779ecb','font-weight':'bold'})),
                                                dbc.CardBody(
                                                  [ 
                                                        ######
                                                        vis2.viz2_layout,
                                                        #######
                                                    ],
                                                    id="graph-body-2",
                                                   style={'display': 'block','background':'#779ecb'}
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
                                                               id="graph-title-3"
                                                                ,style={'background':'#779ecb','font-weight':'bold'}   
                                                                         )),
                                                dbc.CardBody(
                                                    [
                                                        #####
                                                        viz_3.layout
                                                        #####
                                                    ],
                                                    id="graph-body-3",
                                                    style={'display': 'block','background':'#779ecb'}
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
                                                    "Graph 4: " + viz4_title, className="graph-title", id="graph-title-4"
                                                     ,style={'background':'#779ecb','font-weight':'bold'}
                                                )),
                                                dbc.CardBody(
                                                    [
                                                      #########
                                                      vis4.vis4_layout  ,
                                                      ##########
                                                    ],
                                                    id="graph-body-4",
                                                    style={'display': 'block','background':'#779ecb'}
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
                                                    "Graph 5: " + viz5_title, className="graph-title", id="graph-title-5"
                                                 ,style={'background':'#779ecb','font-weight':'bold'}
                                                )),  
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
                                                   style={'display': 'block','background':'#779ecb'}
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
                                                    "Graph 6: " + viz6_title, className="graph-title", id="graph-title-6"
                                                 ,style={'background':'#779ecb','font-weight':'bold'}
                                                )),
                                                dbc.CardBody(
                                                    [
                                                        #####
                                                        vis6.layout
                                                        #####
                                                    ],
                                                    id="graph-body-6",
                                                    style={'display': 'block','background':'#779ecb'}
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

register_callbacks(app,vis1.dict_data_site,vis1.variables,vis1.df_dense,vis2_bubble_df,vis5_df,dataframe)

if __name__ == "__main__":
    app.run_server(debug=True)
