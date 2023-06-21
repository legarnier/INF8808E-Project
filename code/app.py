import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

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
                        html.Button(
                            "Visualization 5",
                            id="button-5",
                            n_clicks=0,
                            className="button-style",
                        ),
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
                )], style={"display": "flex"}),
    ],
)


@app.callback(
    Output("plot-text", "children"),
    Input("button-1", "n_clicks"),
    Input("button-2", "n_clicks"),
    Input("button-3", "n_clicks"),
    Input("button-4", "n_clicks"),
    Input("button-5", "n_clicks"),
    Input("button-6", "n_clicks"),
)
def update_plot(*button_clicks):
    button_texts = [
        "Visualization 1",
        "Visualization 2",
        "Visualization 3",
        "Visualization 4",
        "Visualization 5",
        "Visualization 6",
    ]
    triggered_button_id = dash.callback_context.triggered[0]["prop_id"].split(".")[
        0]
    if triggered_button_id:
        button_index = int(triggered_button_id.split("-")[1]) - 1
        return button_texts[button_index]
    return ""
