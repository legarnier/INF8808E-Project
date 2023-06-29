
import json
import plotly.graph_objects as go
from . import  map_viz
from . import helper
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc


#viz_3 preprocessing
def to_df(data):
    # Convert JSON formatted data to dataframe
    return pd.json_normalize(data['features'])
def get_neighborhoods(data):
    return to_df(data)['properties.prov_name_en'].unique()

#read the data from csv (scatter part)
df_viz3 = pd.read_csv('../data/map_data.csv')

#read the geojson data (map part)
with open('../data/georef-canada-province@public.geojson', encoding='utf-8') as data_file:
    map_data = json.load(data_file)

#draw maps 
locations = get_neighborhoods(map_data)
z = len(map_data['features']) * [1]
fig = go.Figure()
fig = map_viz.add_choro_trace(fig, map_data, locations, z)
fig = map_viz.add_scatter_traces(fig, df_viz3)

#add style to the map
fig = helper.adjust_map_style(fig)
fig = helper.adjust_map_sizing(fig)
fig = helper.adjust_map_info(fig)
fig.update_layout(height=500, width=1000)

#viz 3 layout

layout = html.Div(
    style={
        'display': 'flex'
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
                                             'margin': '2px'
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
                                     'margin': '2px 42px 2px 0',
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
        )])
