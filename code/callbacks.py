#We put all our callbacks here instead of app.py

import dash
from dash.dependencies import Input, Output, State
import preprocess
from dash import dcc, html
import pandas as pd
import vis2,vis6,vis5,vis1,vis4,viz3
from datetime import date

# # Updating the current latencies
def register_callbacks(app,dict_data_site,variables,df_dense,vis2_bubble_df,vis5_df,dataframe):
    @app.callback(
        Output("gauges-container", "children"),
        [
            Input("button-site-qc", "n_clicks"),
            Input("button-site-on", "n_clicks"),
            Input("button-site-man", "n_clicks"),
            Input("radio-type", "value"),
            Input("interval-component", "n_intervals")
        ],
    )
    def update_gauges(site_qc_clicks, site_on_clicks, site_man_clicks, radio_type_value, n_intervals):
        ctx = dash.callback_context
        button_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else "button-site-qc"

        if button_id == "button-site-qc":
            selected_data = dict_data_site['Quebec'][radio_type_value]
        elif button_id == "button-site-on":
            selected_data = dict_data_site['Ontario'][radio_type_value]
        elif button_id == "button-site-man":
            selected_data = dict_data_site['Manitoba'][radio_type_value]
        else:
            selected_data = dict_data_site['Quebec'][radio_type_value]

        row_index = n_intervals % len(selected_data)
        ref_index = row_index - 1
        gauges = []
        for i, variable in enumerate(variables):
            figure = preprocess.generate_gauge_figure(selected_data.iloc[row_index][variable], variable,selected_data.iloc[ref_index][variable])
            gauges.append(
                dcc.Graph(
                    id=f"gauge{i+1}",
                    figure=figure,
                    config={"displayModeBar": False},
                    style={"height": "200px", "width": "16.66%", "margin": "0"},
                )
            )

        return gauges



    # apply filters on graph 2
    @app.callback(
        Output('fig2-bubble', 'figure'),
        [Input('filter_date', 'start_date'),
        Input('filter_date', 'end_date'),
        Input('filter_protocol', 'value')]
    )
    def update_output(start_date, end_date, value):
        dataframe = pd.read_csv('../data/dataset.csv')
        if value == 'All' and start_date is None:
            fig2 = vis2.buble_chart(vis2_bubble_df)
        elif value != 'All' and start_date is None:
            protocol_df = preprocess.filter_protocol(dataframe, value)
            vis2_df_filtered = preprocess.bubble_chart_df(protocol_df)
            fig2 = vis2.buble_chart(vis2_df_filtered)
        elif value == 'All' and start_date is not None and end_date is not None:
            start_date_object = date.fromisoformat(start_date)
            end_date_object = date.fromisoformat(end_date)

            date_df = preprocess.filter_date(
                dataframe, start_date_object, end_date_object)
            vis2_df_filtered = preprocess.bubble_chart_df(date_df)
            fig2 = vis2.buble_chart(vis2_df_filtered)
        else:
            start_date_object = date.fromisoformat(start_date)
            end_date_object = date.fromisoformat(end_date)

            date_df = preprocess.filter_date(
                dataframe, start_date_object, end_date_object)
            filtered_df = preprocess.filter_protocol(date_df, value)
            vis2_df_filtered = preprocess.bubble_chart_df(filtered_df)
            fig2 = vis2.buble_chart(vis2_df_filtered)

        return fig2

    # Graph2: change line chart based in the clicked point on bubble chart


    @app.callback(
        Output('fig2-line', 'figure'),
        [Input('fig2-bubble', 'clickData'),
        Input('filter_date', 'start_date'),
        Input('filter_date', 'end_date'),
        Input('filter_protocol', 'value')]
    )
    def bubble_clicked(bubble_clicked, start_date, end_date, protocol):
        dataframe = pd.read_csv('../data/dataset.csv')
        if bubble_clicked is None:
            fig2_line = vis2.get_empty_figure()

        # draw line chart without any filetr
        elif bubble_clicked is not None and start_date is None and protocol == 'All':
            application_type = preprocess.bubble_select(dataframe, date(
                2023, 6, 1), date(2023, 6, 5), protocol, bubble_clicked)
            if application_type == None:
                fig2_line = vis2.get_empty_figure()
            else:
                vis2_line_df = preprocess.line_chart_df(
                    dataframe, application_type, date(2023, 6, 1), date(2023, 6, 5))
                fig2_line = vis2.line_chart(vis2_line_df, application_type)

        elif start_date is not None and protocol == 'All':  # draw line chart based on date range filter only
            start_date_object = date.fromisoformat(start_date)
            end_date_object = date.fromisoformat(end_date)
            application_type = preprocess.bubble_select(
                dataframe, start_date_object, end_date_object, protocol, bubble_clicked)
            if application_type == None:
                fig2_line = vis2.get_empty_figure()
            else:
                date_df = preprocess.filter_date(
                    dataframe, start_date_object, end_date_object)
                vis2_line_df = preprocess.line_chart_df(
                    date_df, application_type, start_date_object, end_date_object)
                fig2_line = vis2.line_chart(vis2_line_df, application_type)

        elif start_date is None and protocol != 'All':  # draw the line chart based on protocol filter only
            application_type = preprocess.bubble_select(dataframe, date(
                2023, 6, 1), date(2023, 6, 5), protocol, bubble_clicked)

            if application_type == None:
                fig2_line = vis2.get_empty_figure()
            else:
                filtered_df = preprocess.filter_protocol(dataframe, protocol)
                vis2_line_df = preprocess.line_chart_df(
                    filtered_df, application_type,  date(2023, 6, 1), date(2023, 6, 5))
                fig2_line = vis2.line_chart(vis2_line_df, application_type)

        else:  # draw the line chart based on filters and bubble clicked
            start_date_object = date.fromisoformat(start_date)
            end_date_object = date.fromisoformat(end_date)
            application_type = preprocess.bubble_select(
                dataframe, start_date_object, end_date_object, protocol, bubble_clicked)

            if application_type == None:
                fig2_line = vis2.get_empty_figure()
            else:
                date_df = preprocess.filter_date(
                    dataframe, start_date_object, end_date_object)
                filtered_df = preprocess.filter_protocol(date_df, protocol)
                vis2_line_df = preprocess.line_chart_df(
                    filtered_df, application_type, start_date_object, end_date_object)
                fig2_line = vis2.line_chart(vis2_line_df, application_type)

        return fig2_line



    @app.callback(
        Output("graph-body-1", "style"),
        Input("graph-title-1", "n_clicks"),
        Input("button-1", "n_clicks")
        ,State('graph-body-1', 'style')
    )
    @app.callback(
        Output("graph-body-2", "style"),
        Input("graph-title-2", "n_clicks"),
        Input("button-2", "n_clicks")
        ,State('graph-body-2', 'style')

    )
    @app.callback(
        Output("graph-body-3", "style"),
        Input("graph-title-3", "n_clicks"),
        Input("button-3", "n_clicks")
            ,State('graph-body-3', 'style')

    )
    @app.callback(
        Output("graph-body-4", "style"),
        Input("graph-title-4", "n_clicks"),
        Input("button-4", "n_clicks")
        ,State('graph-body-4', 'style')

    )
    @app.callback(
        Output("graph-body-5", "style"),
        Input("graph-title-5", "n_clicks"),
        Input("button-5", "n_clicks")
        ,State('graph-body-5', 'style')

    )
    @app.callback(
        Output("graph-body-6", "style"),
        Input("graph-title-6", "n_clicks"),
        Input("button-6", "n_clicks")
        ,State('graph-body-6', 'style')

    )
    def toggle_content(open_clicks, close_clicks, style):
        
        if open_clicks is None and close_clicks is None:
            return style  # No button clicks yet, maintain current style
        display = style.get('display', 'block')

        new_style = {'display': 'none'} if display == 'block' else {'display': 'block'}
        return new_style



    @app.callback(
        Output('heatmap', 'figure'),
        Input('place', 'value'),
        Input('type', 'value'))
    def vis6_update_heatmap(place, typ):

        # Update the heatmap figure
        fig = vis6.update_heatmap(df_dense,
                                place,
                                typ)
        return fig


    @app.callback(
        Output('linegraph', 'figure'),
        Input('heatmap', 'clickData'),
        Input('zoom_level', 'value'),
        Input('place', 'value'),
        Input('type', 'value'),
    )
    def vis6_update_line(clickData, zoom_level, place, typ):

        # Update the line graph
        fig = vis6.update_line(df_dense, clickData, zoom_level, place, typ)
        return fig


    # Callback for updating the animation graph and buttons
    @app.callback(
        dash.dependencies.Output('animation-graph', 'figure'),
        dash.dependencies.Input('button-dropdown', 'value')
    )

    def update_graph(button_value):
    
        fig = vis4.update_graph(button_value,dataframe)
        return fig
            

    @app.callback(
        Output('fig5', 'figure'),
        Input('viz5_places', 'value')
    )
    def vis5_update_linechart(viz5_places):

        # Create the line chart figure
        fig = vis5.update_vis5(vis5_df.loc[vis5_df['Site'] == viz5_places], viz5_places)
        return fig

    # Callbacks for the download button
    @app.callback(
        Output("download-text", "data"),
        Input("btn-download", "n_clicks"),
        prevent_initial_call=True,
    )
    def func1(n_clicks):
        return dcc.send_file("../data/Project Description.pdf")
