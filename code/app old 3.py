import dash
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Row(
            [
                # Sidebar
                dbc.Col(
                    dbc.Nav(
                        [
                            dbc.NavLink("Link 1", href="/link1"),
                            dbc.NavLink("Link 2", href="/link2"),
                            dbc.NavLink("Link 3", href="/link3"),
                        ],
                        vertical=True,
                        pills=True,
                    ),
                    width=2,  # Adjust the width as per your requirements
                    className="sidebar",  # Custom CSS class for sidebar
                ),
                # Graph Boxes
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.H1("Project Description", className="project-title"),
                                html.H3("Team Number: 12345", className="team-number"),
                                html.H3("Date: June 30, 2023", className="date"),
                            ],
                            className="header-container",
                        ),
                        dbc.Alert(
                            "Graph 1 Content",
                            id="graph-alert-1",
                            color="info",
                            dismissable=True,
                            className="graph-box",
                        ),
                        dbc.Alert(
                            "Graph 2 Content",
                            id="graph-alert-2",
                            color="info",
                            dismissable=True,
                            className="graph-box",
                        ),
                        dbc.Alert(
                            "Graph 3 Content",
                            id="graph-alert-3",
                            color="info",
                            dismissable=True,
                            className="graph-box",
                        ),
                        dbc.Alert(
                            "Graph 4 Content",
                            id="graph-alert-4",
                            color="info",
                            dismissable=True,
                            className="graph-box",
                        ),
                        dbc.Alert(
                            "Graph 5 Content",
                            id="graph-alert-5",
                            color="info",
                            dismissable=True,
                            className="graph-box",
                        ),
                        dbc.Alert(
                            "Graph 6 Content",
                            id="graph-alert-6",
                            color="info",
                            dismissable=True,
                            className="graph-box",
                        ),
                    ],
                    width=9,
                    className="graph-area",
                ),
            ],
            className="main-row",
        ),
    ],
    id="main-container"  # Add an ID to the main container for JavaScript functionality
)

"


if __name__ == "__main__":
    app.run_server(debug=True)
