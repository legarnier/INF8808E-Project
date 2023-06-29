
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

#add hover 
def map_base_hover_template():
    # Generate the hover template
    return '<span style="font-family: Oswald">    %{properties.prov_name_en}</span>' + '<extra></extra>'

def map_marker_hover_template(name):
    # Generate the hover template
    return f'<span style="font-family: Oswald"> {name}</span>' + '<extra></extra>'

#display map
def add_choro_trace(fig, data, locations, z_vals):
    colorscale = ['#CDD1C4', '#CDD1C4']
    # Draw the map base
    fig.add_trace(
        go.Choroplethmapbox(
            geojson=data,
            locations=locations,
            z=z_vals,
            colorscale=colorscale,
            marker_opacity=0.2,
            featureidkey='properties.prov_name_en',
            showscale=False,
        )
    )

    # Set hovertemplate for the figure
    hover_temp = map_base_hover_template()
    fig.update_traces(hovertemplate=hover_temp)
    return fig

#add scatters on the map
def add_scatter_traces(fig, trace_data):
    # get range of the circles
    latency_min = np.min(trace_data['Latency'])
    latency_max = np.max(trace_data['Latency'])

    # Define the scaling factor for marker sizes
    scaling_factor = 0.5

    # Scale down the maximum marker size
    scaled_max_size = latency_max * scaling_factor
    scaled_min_size = latency_min * scaling_factor

    scatter = px.scatter_mapbox(trace_data,
                                lat="Latitude",
                                lon="Longitude",
                                color='Protocol',
                                size="Latency",
                                size_max=scaled_max_size,
                                opacity=1)

    # Set min marker size and make circles empty
    scatter.update_traces(mode='markers',
                          marker=dict(#symbol='circle-open',
                                      sizemin=scaled_min_size,
                                     ),
                          selector=dict(type='scattermapbox'))
    fig.add_traces(scatter.data)
    return fig
