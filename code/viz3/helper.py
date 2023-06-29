
import plotly.graph_objects as go


def adjust_map_style(fig):
    fig.update_layout(mapbox_style='white-bg')
    return fig


def adjust_map_sizing(fig):
    fig.update_layout(mapbox_center=go.layout.mapbox.Center(
        lat=45.569260,
        lon=-73.707014))
    fig.update_layout(mapbox_zoom=3)
    fig.update_layout(height=525, width=1000)
    return fig


def adjust_map_info(fig):
    fig.update_layout(legend_x=0.70,
                      legend_y=0.95)

    fig.update_layout(title_xref='paper', title_y=0.5)

    title = 'Current latency in Quebec, Ontario and Manitoba'
    info = 'Click on each protocol for filtering'

    fig.update_layout(title=title,
                      title_font_family='Oswald',
                      title_font_color='black',
                      title_font_size=28)
    fig.update_layout(annotations=[dict(xref='paper',
                                        yref='paper',
                                        x=0.055, y=1.08,
                                        showarrow=False,
                                        text=info,
                                        font_family='Open Sans Condensed',
                                        font_color='black',
                                        font_size=18)])
    fig.update_layout(legend_title_text='Protocols',
                      legend_title_font_family='Open Sans Condensed',
                      legend_title_font_color='black',
                      legend_title_font_size=16,
                      legend_font_family='Open Sans Condensed',
                      legend_font_color='black',
                      legend_font_size=16)

    return fig
