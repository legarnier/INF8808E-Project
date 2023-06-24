
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def gauge_chart(variables,values):
 
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
            y=1,
            text='',
            showarrow=False,
            textangle=0,
            xanchor='center',
            yanchor='middle',
            font=dict(size=12, color='black'),
            opacity=0.8
        )

    fig.update_layout(
        grid={'rows': 1, 'columns': len(variables), 'pattern': "independent"},
        height=230,
        width=1200,  # Ajouter de la marge autour de la figure
        template='plotly_white',  # Utiliser un thème de couleur clair
    )

    return(fig)