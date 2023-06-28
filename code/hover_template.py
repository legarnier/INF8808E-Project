'''
    This file contains the code for the whole project.
'''

def hover_vis5_forcasting_range(y_mins, y_values , y_maxs,conf_lev,vol):
    
      # create hover text for main line
    hover_template = """<b>Time: %{x}</b>
                        <br><span style="color:blue;">Total Latency: %{y:.2f}</span>
                        <br><span style="color:red;">Forecasting Range: (%{customdata[1]:.2f}ms to %{customdata[0]:.2f}ms)</span>

                        <br><span style="color:purple;">Confidence level: %{customdata[2]:.2f}</span>
                        <br><span style="color:brown;">Volatility level: %{customdata[3]:.2f}</span>
                        <extra></extra>'
                     """

    return(hover_template)