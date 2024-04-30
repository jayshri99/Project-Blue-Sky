import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import numpy as np
import os
import utils

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Project Blue Sky", style={'textAlign': 'center', 'font-family': 'Helvetica'}),
    html.H2("Part I. General Visualization", style={'textAlign': 'left', 'font-family': 'Helvetica'}),
    html.Div([
        html.Label('Select states: ', style={'display': 'inline-block', 'margin-right': '10px', 'font-weight': 'bold', 'font-family': 'Helvetica'}),

        # Use a Div to hold the checklist, with an internal style for wrapping
        html.Div(
            dcc.Checklist(
                id='general_state',
                options=utils.US_STATES_OPTIONS,
                value=['Illinois'],  # Default selected state(s)
                labelStyle={'display': 'inline-block', 'width': '150px'}  # Adjust width as needed
            ), 
            style={'columnCount': 5}  # Create 5 columns; adjust as needed for your layout
        ),

        html.Div([
            html.Label('Select a AQI Metric: ', style={'display': 'inline-block', 'margin-right': '10px', 'font-weight': 'bold', 'font-family': 'Helvetica'}),
            dcc.Dropdown(
                id='AQI_metric',
                options=[
                    {'label': 'General AQI Index', 'value': 'AQI'},
                    {'label': 'Carbon Monoxide (CO)', 'value': 'CO AQI'},
                    {'label': 'Nitrogen Dioxide (NO2)', 'value': 'NO2 AQI'},
                    {'label': 'Ozone (O3)', 'value': 'Ozone AQI'},
                    {'label': 'Iinhalable Particles (PM10)', 'value': 'PM10 AQI'},
                    {'label': 'Iinhalable Particles (PM2.5)', 'value': 'PM2.5 AQI'},
                ],
                value='AQI'
            ),
        ], style={'margin-bottom': '10px', 'font-family': 'Helvetica'}),

        html.Label('Select A Date Range:', style={'display': 'inline-block', 'margin-right': '10px', 'margin-left': '10px', 'font-weight': 'bold', 'font-family': 'Helvetica'}),
        dcc.DatePickerRange(
            id='date_range_general',
            start_date='1980-01-01',
            end_date='2021-12-31'
        ),
        dcc.Graph(id='General'),

        
        html.H2("Part II. Heatmap Visualization", style={'textAlign': 'left'}),
        html.Label('Select A Date for colormap:', style={'display': 'inline-block', 'margin-right': '10px', 'margin-left': '10px', 'font-weight': 'bold', 'font-family': 'Helvetica'}),
        dcc.DatePickerSingle(
            id='colormap_date',
            date='2021-01-01'
        ),
        html.Div([
            html.Label('Select a AQI Metric for map display: ', style={'display': 'inline-block', 'margin-right': '10px', 'font-weight': 'bold', 'font-family': 'Helvetica'}),
            dcc.Dropdown(
                id='AQI_metric2',
                options=[
                    {'label': 'General AQI Index', 'value': 'AQI'},
                    {'label': 'Carbon Monoxide (CO)', 'value': 'CO AQI'},
                    {'label': 'Nitrogen Dioxide (NO2)', 'value': 'NO2 AQI'},
                    {'label': 'Ozone (O3)', 'value': 'Ozone AQI'},
                    {'label': 'Iinhalable Particles (PM10)', 'value': 'PM10 AQI'},
                    {'label': 'Iinhalable Particles (PM2.5)', 'value': 'PM2.5 AQI'},
                ],
                value='AQI'
            ),
        ], style={'margin-bottom': '10px', 'font-family': 'Helvetica'}),
        # html.Label('Heatmap for each state (AQI and Gas Price)', style={'display': 'inline-block', 'margin-right': '10px'}),
        dcc.Graph(id='Colormap')
    ])
])

@app.callback(
    Output('General', 'figure'),
    [Input('general_state', 'value'), 
     Input('AQI_metric', 'value'), 
     Input('date_range_general', 'start_date'), 
     Input('date_range_general', 'end_date')]
)
def update_General_Plot(selected_states, aqi_metric, start_date, end_date):
    fig_general = utils.get_general_plot(selected_states, aqi_metric, start_date, end_date)

    return fig_general

@app.callback(
     Output('Colormap', 'figure'),
    [Input('AQI_metric2', 'value'), 
     Input('colormap_date', 'date')]
)
def update_General_Plot(aqi_metric2, colormap_date):
    fig_colormap = utils.get_colormap(aqi_metric2, colormap_date)

    return fig_colormap

if __name__ == '__main__':
    app.run_server(debug=True)
