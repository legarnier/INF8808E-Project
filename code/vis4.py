import plotly.graph_objects as go
import pandas as pd

def animated_line(df):

    #df = pd.read_csv('INF8808E.csv')
    df.drop(['Protocol', 'Latency'], axis=1, inplace=True)
    df = df.groupby(['Site', 'Time', 'Type'], as_index=False)['Average Latency'].mean()

    app_df = df[df['Type'] == 'app'].rename(columns={'Average Latency': 'app_Average_Latency'})
    network_df = df[df['Type'] == 'network'].rename(columns={'Average Latency': 'network_Average_Latency'})

    # Merge the dataframes on 'Site' and 'Time' with explicit suffixes

    df = pd.merge(app_df, network_df, on=['Site', 'Time'], suffixes=('_app', '_network'))
    df.drop(['Type_network', 'Type_app'], axis=1, inplace=True)

    #display(df)




    # Base plot
    fig = go.Figure(
        layout=go.Layout(
            updatemenus=[dict(type="buttons", direction="right", x=0.9, y=1.16), ],
            xaxis=dict(
                range=["6-1-2023", "6-5-2023"],
                    autorange=False, tickwidth=5,
                    title_text="Time"),
            yaxis=dict(range=[45, 85],
                    autorange=False,
                    title_text="Average Latency"),
            title="Latency averages for each site based on type",
        ))

    # Add traces
    init = 1

    fig.add_trace(
        go.Scatter(x=df.Time[:init], y=df[df.Site == 'Quebec'].network_Average_Latency[:init], name='Quebec',
                visible=True,
                line=dict(color="#FF0000", dash="solid")))
    fig.add_trace(
        go.Scatter(x=df.Time[:init], y=df[df.Site == 'Ontario'].network_Average_Latency[:init], name='Ontario',
                visible=True,
                line=dict(color="#00FF00", dash="solid")))
    fig.add_trace(
        go.Scatter(x=df.Time[:init], y=df[df.Site == 'Manitoba'].network_Average_Latency[:init], name='Manitoba',
                visible=True,
                line=dict(color="#0000FF", dash="solid")))
    fig.add_trace(
        go.Scatter(x=df.Time[:init], y=df[df.Site == 'Quebec'].app_Average_Latency[:init], name='Quebec',
                visible=True,
                line=dict(color="#FF0000", dash="dash")))
    fig.add_trace(
        go.Scatter(x=df.Time[:init], y=df[df.Site == 'Ontario'].app_Average_Latency[:init], name='Ontario',
                visible=True,
                line=dict(color="#00FF00", dash="dash")))
    fig.add_trace(
        go.Scatter(x=df.Time[:init], y=df[df.Site == 'Manitoba'].app_Average_Latency[:init], name='Manitoba',
                visible=True,
                line=dict(color="#0000FF", dash="dash")))

    # fig.add_trace(
    #     go.Scatter(x=df.Time[:init],
    #                y=df.app_Average_Latency[:init],
    #                name="Average Latency",
    #                visible=True,
    #                line=dict(color="#bf00ff", dash="dash")))

    # Animation
    fig.update(frames=[
        go.Frame(
            data=[
                go.Scatter(x=df.Time[:k], y=df[df.Site == 'Quebec'].network_Average_Latency[:k], name='Quebec'),
                go.Scatter(x=df.Time[:k], y=df[df.Site == 'Ontario'].network_Average_Latency[:k], name='Ontario'),
                go.Scatter(x=df.Time[:k], y=df[df.Site == 'Manitoba'].network_Average_Latency[:k], name='Manitoba'),
                go.Scatter(x=df.Time[:k], y=df[df.Site == 'Quebec'].app_Average_Latency[:k], name='Quebec'),
                go.Scatter(x=df.Time[:k], y=df[df.Site == 'Ontario'].app_Average_Latency[:k], name='Ontario'),
                go.Scatter(x=df.Time[:k], y=df[df.Site == 'Manitoba'].app_Average_Latency[:k], name='Manitoba'),            
            ],
            name=f'frame{k}'
        )
        for k in range(init, len(df)+1)
    ])

    # Extra Formatting
    ##print(len(df.Time.unique()))
    fig.update_xaxes(range=[0,len(df.Time.unique())], ticks="outside", tickwidth=2, tickcolor='grey', ticklen=12)
    fig.update_yaxes(ticks="outside", tickwidth=2, tickcolor='white', ticklen=1)
    fig.update_layout(yaxis_tickformat=',')
    #fig.update_layout(legend=dict(x=0, y=1.1), legend_orientation="h")
    fig.update_layout(legend=dict(x=1.02, y=0.98), 
                    legend_orientation="v",
                    #itemclick="toggle", 
                    template="plotly",
                    margin=dict(l=10, r=10, t=10, b=10)
                    )


    # Buttons
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label="Play",
                            method="animate",
                        args=[None, {"frame": {"duration": 1000}}]),
                    dict(label="Applicatin",
                        method="update",
                        args=[{"visible": [False, True]},
                            {"showlegend": True}]),
                    dict(label="Network",
                        method="update",
                        args=[{"visible": [True, False]},
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
                #buttonsize=1.5,
                pad={"r": 10, "t": 10},
            )])
    
    return(fig)
    #fig.show()

