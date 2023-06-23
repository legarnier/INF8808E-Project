import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def initial(variables,values):
 
    fig = go.Figure()
    # need to define types of subplots...
    fig = make_subplots(
        rows=len(values),
        cols=len(variables),
        specs=[[{"type": "indicator"} for c in variables] for t in values],
    )
    for i in range(len(variables)):
        domain_start = i * (1 / 6)
        domain_end = (i + 1) * (1 / 6)
        domain_center = (domain_start + domain_end) / 2

        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=values[i],
            title={'text': variables[i]},
            delta={'reference': 65},
            domain={'row': 0, 'column': i},
            gauge={'axis': {'range': [None, 100]},
                'bar': {'color': 'rgb(0, 128, 255)'},
                'bgcolor': 'white',
                'borderwidth': 2,
                'bordercolor': 'gray',
                'steps': [
                    {'range': [0, values[i]], 'color': 'rgb(0, 70, 140)'},  # Couleur rouge pour l'augmentation
                    {'range': [values[i], 100], 'color': 'rgb(0, 128, 255)'}],  # Couleur bleue pour le reste

                }))

        fig.add_annotation(
            x=domain_center,
            y=0.25,
            text='',
            showarrow=False,
            textangle=0,
            xanchor='center',
            yanchor='middle',
            font=dict(size=16, color='black'),
            opacity=0.8
        )

    fig.update_layout(
        title='Protocol latencies',
        grid={'rows': 1, 'columns': len(variables), 'pattern': "independent"},
        height=800,
        width=1500,
        margin=dict(l=100, r=100, b=100, t=100),  # Ajouter de la marge autour de la figure
        template='plotly_white',  # Utiliser un thème de couleur clair
    )

    return(fig)


def update_figure(interval):

    # Génération de nouvelles données
    variables = ['HTTPS', 'HTTP', 'TCP', 'ICMP', 'TWAMP','UDP']
    values = [75, 60, 90, 45, 80,78]
    random.shuffle(values) 
    # Ajout du nouveau trace à la figure
    
    fig = initial(variables,values)
    return fig
