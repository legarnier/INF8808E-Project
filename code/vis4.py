

import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from datetime import date
import preprocess

import hover
def update_graph(button_value,df_viz4):
   # Data Preparation
    #df_viz4 = pd.read_csv('../data/dataset.csv')

    df_viz4 = preprocess.city_average_latency_type(df_viz4)

    # Add Traces

    init = 1

    fig = go.Figure(
        layout=go.Layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(label="Play",
                             method="animate",
                             args=[None, {"frame": {"duration": 1000}}]),
                        dict(label="Application",
                             method="update",
                             args=[{"visible": [False, False, False, True, True, True]},
                                   {"showlegend": True}]),
                        dict(label="Network",
                             method="update",
                             args=[{"visible": [True, True, True, False, False, False]},
                                   {"showlegend": True}]),
                        dict(label="Both Types",
                             method="update",
                             args=[{"visible": [True, True, True]},
                                   {"showlegend": True}]),
                    ]),
                    x=1.2,
                    y=0.35,
                    xanchor="right",
                    yanchor="middle",
                    direction="down",
                    pad={"r": 10, "t": 10},
                )
            ],
            xaxis=dict(
                #range=["6-1-2023", "6-5-2023"]
                
                range= [date(2023, 6, 1), date(2023, 6, 5)],

                autorange=False, tickwidth=5,
                title_text="Time"),
            
            yaxis=dict(range=[45, 85],
                       autorange=False,
                       title_text="Average Latency"),
            #title="Latency averages for each site based on type",
        )
    )
   
   # ########################################################################################
   # add traces to the graph
   # Individual lines on the graph are represented by traces. 
   # There are different visual properties associated with each trace, such as line color, 
   # line style, and hover information, based on the data used in the df_viz4 DataFrame
   # ########################################################################################

   
    fig.add_trace(
        go.Scatter(x=df_viz4.Time[:init], y=df_viz4[df_viz4.Site == 'Quebec'].network_Average_Latency[:init], name='Quebec(Network)',
               visible=True,
               line=dict(color="#17becf", dash="solid"),
               hovertemplate='<b>Site:</b> Quebec<br><b>Time:</b> %{x}<br><b>Average Latency:</b> %{y}<br><b>Type:</b> Network<extra></extra>')

    )
    
    fig.add_trace(
        go.Scatter(x=df_viz4.Time[:init], y=df_viz4[df_viz4.Site == 'Ontario'].network_Average_Latency[:init], name='Ontario(Network)',
               visible=True,
               line=dict(color="#ff7f0e", dash="solid"),
               hovertemplate='<b>Site:</b> Ontario<br><b>Time:</b> %{x}<br><b>Average Latency:</b> %{y}<br><b>Type:</b> Network<extra></extra>')
    )
    
    fig.add_trace(
        go.Scatter(x=df_viz4.Time[:init], y=df_viz4[df_viz4.Site == 'Manitoba'].network_Average_Latency[:init], name='Manitoba(Network)',
               visible=True,
               line=dict(color="#7f7f7f", dash="solid"),
               hovertemplate='<b>Site:</b> Manitoba<br><b>Time:</b> %{x}<br><b>Average Latency:</b> %{y}<br><b>Type:</b> Network<extra></extra>')
    )
    
    fig.add_trace(
        go.Scatter(x=df_viz4.Time[:init], y=df_viz4[df_viz4.Site == 'Quebec'].app_Average_Latency[:init], name='Quebec(Application)',
               visible=True,
               line=dict(color="#17becf", dash="dash"),
               hovertemplate='<b>Site:</b> Quebec<br><b>Time:</b> %{x}<br><b>Average Latency:</b> %{y}<br><b>Type:</b> Application<extra></extra>')
    )
    
    
    fig.add_trace(
        go.Scatter(x=df_viz4.Time[:init], y=df_viz4[df_viz4.Site == 'Ontario'].app_Average_Latency[:init], name='Ontario(Application)',
               visible=True,
               line=dict(color="#ff7f0e", dash="dash"),
               hovertemplate='<b>Site:</b> Ontario<br><b>Time:</b> %{x}<br><b>Average Latency:</b> %{y}<br><b>Type:</b> Application<extra></extra>')
    )
    
    fig.add_trace(
        go.Scatter(x=df_viz4.Time[:init], y=df_viz4[df_viz4.Site == 'Manitoba'].app_Average_Latency[:init], name='Manitoba(Application)',
               visible=True,
               line=dict(color="#7f7f7f", dash="dash"),
               hovertemplate='<b>Site:</b> Manitoba<br><b>Time:</b> %{x}<br><b>Average Latency:</b> %{y}<br><b>Type:</b> Application<extra></extra>')
    )

    

##############################################################################################
#Frames in this graph are used for animation and represen
# different subsets of the df_viz4 DataFrame.Each frame corresponds  
# to a specific point in time and includes traces that display the data  
# for that particular time point. For each frame, a trace represents the average latency 
# data for sites "Quebec",  "Ontario", and "Manitoba" under the "Network" and "Application" types.
# By updating the frames and advancing through them, the graph can be animated to show 
# the changes in latency over time for different sites and types.
##############################################################################################

   
    fig.update(frames=[
        go.Frame(
            data=[
                go.Scatter(x=df_viz4.Time[:k], y=df_viz4[df_viz4.Site == 'Quebec'].network_Average_Latency[:k], name='Quebec(Network)'),
                go.Scatter(x=df_viz4.Time[:k], y=df_viz4[df_viz4.Site == 'Ontario'].network_Average_Latency[:k], name='Ontario(Network)'),
                go.Scatter(x=df_viz4.Time[:k], y=df_viz4[df_viz4.Site == 'Manitoba'].network_Average_Latency[:k], name='Manitoba(Network)'),
                go.Scatter(x=df_viz4.Time[:k], y=df_viz4[df_viz4.Site == 'Quebec'].app_Average_Latency[:k], name='Quebec(Application)'),
                go.Scatter(x=df_viz4.Time[:k], y=df_viz4[df_viz4.Site == 'Ontario'].app_Average_Latency[:k], name='Ontario(Application)'),
                go.Scatter(x=df_viz4.Time[:k], y=df_viz4[df_viz4.Site == 'Manitoba'].app_Average_Latency[:k], name='Manitoba(Application)'),
            ],
            name=f'frame{k}'
        )
        for k in range(init, len(df_viz4) + 1)
    ])

   ####################################################
   # Extra Formatting - graph layout and configuration
   ####################################################
   
    fig.update_layout(plot_bgcolor='#FAF9F6')
    fig.update_xaxes(range=[date(2023, 6, 1),  date(2023, 6, 5)], ticks="outside", tickwidth=2, tickcolor='grey', ticklen=12)
    fig.update_yaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=1)
    fig.update_layout(yaxis_tickformat=',')
    fig.update_layout(legend=dict(x=1.02, y=0.98),
                      legend_orientation="v",
                      template="plotly",
                      margin=dict(l=10, r=10, t=10, b=10)
                      )
    
    
    fig.update_layout(
        
        yaxis_ticksuffix=" ms",
        
        coloraxis_colorbar_ticksuffix="m",
       
    )

    return fig







