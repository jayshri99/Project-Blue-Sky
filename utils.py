import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import os

US_STATES_OPTIONS = [
    {'label': 'Alabama', 'value': 'Alabama'},
    {'label': 'Alaska', 'value': 'Alaska'},
    {'label': 'Arizona', 'value': 'Arizona'},
    {'label': 'Arkansas', 'value': 'Arkansas'},
    {'label': 'California', 'value': 'California'},
    {'label': 'Colorado', 'value': 'Colorado'},
    {'label': 'Connecticut', 'value': 'Connecticut'},
    {'label': 'Delaware', 'value': 'Delaware'},
    {'label': 'Florida', 'value': 'Florida'},
    {'label': 'Georgia', 'value': 'Georgia'},
    {'label': 'Hawaii', 'value': 'Hawaii'},
    {'label': 'Idaho', 'value': 'Idaho'},
    {'label': 'Illinois', 'value': 'Illinois'},
    {'label': 'Indiana', 'value': 'Indiana'},
    {'label': 'Iowa', 'value': 'Iowa'},
    {'label': 'Kansas', 'value': 'Kansas'},
    {'label': 'Kentucky', 'value': 'Kentucky'},
    {'label': 'Louisiana', 'value': 'Louisiana'},
    {'label': 'Maine', 'value': 'Maine'},
    {'label': 'Maryland', 'value': 'Maryland'},
    {'label': 'Massachusetts', 'value': 'Massachusetts'},
    {'label': 'Michigan', 'value': 'Michigan'},
    {'label': 'Minnesota', 'value': 'Minnesota'},
    {'label': 'Mississippi', 'value': 'Mississippi'},
    {'label': 'Missouri', 'value': 'Missouri'},
    {'label': 'Montana', 'value': 'Montana'},
    {'label': 'Nebraska', 'value': 'Nebraska'},
    {'label': 'Nevada', 'value': 'Nevada'},
    {'label': 'New Hampshire', 'value': 'New Hampshire'},
    {'label': 'New Jersey', 'value': 'New Jersey'},
    {'label': 'New Mexico', 'value': 'New Mexico'},
    {'label': 'New York', 'value': 'New York'},
    {'label': 'North Carolina', 'value': 'North Carolina'},
    {'label': 'North Dakota', 'value': 'North Dakota'},
    {'label': 'Ohio', 'value': 'Ohio'},
    {'label': 'Oklahoma', 'value': 'Oklahoma'},
    {'label': 'Oregon', 'value': 'Oregon'},
    {'label': 'Pennsylvania', 'value': 'Pennsylvania'},
    {'label': 'Rhode Island', 'value': 'Rhode Island'},
    {'label': 'South Carolina', 'value': 'South Carolina'},
    {'label': 'South Dakota', 'value': 'South Dakota'},
    {'label': 'Tennessee', 'value': 'Tennessee'},
    {'label': 'Texas', 'value': 'Texas'},
    {'label': 'Utah', 'value': 'Utah'},
    {'label': 'Vermont', 'value': 'Vermont'},
    {'label': 'Virginia', 'value': 'Virginia'},
    {'label': 'Washington', 'value': 'Washington'},
    {'label': 'West Virginia', 'value': 'West Virginia'},
    {'label': 'Wisconsin', 'value': 'Wisconsin'},
    {'label': 'Wyoming', 'value': 'Wyoming'}
]

US_RECESSIONS = [("1980-1-1", "1980-7-15"),
                 ("1981-7-15", "1982-11-30"),
                 ("1990-7-15", "1991-3-15"),
                 ("2001-3-15", "2001-11-15"),
                 ("2007-12-15","2009-6-15"),
                 ("2020-2-1", "2020-4-30")]

US_RAPID_GROWTH = [("1980-7-15", "1981-7-15"),
                 ("1982-11-30", "1990-7-15"),
                 ("1991-3-15", "2001-3-15"),
                 ("2001-11-15","2007-12-15"),
                 ("2009-6-15", "2020-1-31"),
                 ("2020-4-30","2021-12-31")]

US_ECON_DETAILS = {"1980-1-1":{"Name":"1980 recession",
                                     "Peak Unemployment (%)": 7.8,
                                     "GDP Decline (%)": -2.2,
                                     "Details":"https://en.wikipedia.org/wiki/Early_1980s_recession_in_the_United_States#1980"},
                        "1981-7-15":{"Name":"1981-1982 recession",
                                     "Peak Unemployment (%)": 10.8,
                                     "GDP Decline (%)": -2.7,
                                     "Details":"https://en.wikipedia.org/wiki/Early_1980s_recession_in_the_United_States#1981%E2%80%931982"},
                        "1990-7-15":{"Name":"Early 1990s recession",
                                     "Peak Unemployment (%)": 7.8,
                                     "GDP Decline (%)": -1.4,
                                     "Details":"https://en.wikipedia.org/wiki/Early_1990s_recession_in_the_United_States"},
                        "2001-3-15":{"Name":"Early 2000s recession",
                                     "Peak Unemployment (%)": 6.3,
                                     "GDP Decline (%)": -0.3,
                                     "Details":"https://en.wikipedia.org/wiki/Early_2000s_recession"},
                        "2007-12-15":{"Name":"Great Recession 2008",
                                     "Peak Unemployment (%)": 10.0,
                                     "GDP Decline (%)": -5.1,
                                     "Details":"https://en.wikipedia.org/wiki/Great_Recession"},
                        "2020-2-1":{"Name":"COVID-19 recession",
                                     "Peak Unemployment (%)": 14.7,
                                     "GDP Decline (%)": -19.2,
                                     "Details":"https://en.wikipedia.org/wiki/COVID-19_recession"},
                        "1980-7-15":{"Name":"1980-1981 Growth",
                                     "Annual Employment Growth (%)": 2.0,
                                     "Annual GDP Growth (%)": 4.4,
                                     "Details":"https://en.wikipedia.org/wiki/List_of_economic_expansions_in_the_United_States#:~:text=raising%20interest%20rates.-,Jul%201980%E2%80%93%0AJul%201981,-12"},
                        "1982-11-30":{"Name":"1982-1990 Growth",
                                     "Annual Employment Growth (%)": 2.8,
                                     "Annual GDP Growth (%)": 4.3,
                                     "Details":"https://en.wikipedia.org/wiki/List_of_economic_expansions_in_the_United_States#:~:text=dip%20recession.-,Dec%201982%E2%80%93%0AJuly%201990,-92"},
                        "1991-3-15":{"Name":"1992-2001 Growth",
                                     "Annual Employment Growth (%)": 2.0,
                                     "Annual GDP Growth (%)": 3.6,
                                     "Details":"https://en.wikipedia.org/wiki/List_of_economic_expansions_in_the_United_States#:~:text=4%5D%5B5%5D-,Mar%201991%E2%80%93%0AMar%202001,-120"},
                        "2001-11-15":{"Name":"2001-2007 Growth",
                                     "Annual Employment Growth (%)": 0.9,
                                     "Annual GDP Growth (%)": 2.8,
                                     "Details":"https://en.wikipedia.org/wiki/List_of_economic_expansions_in_the_United_States#:~:text=the%20following%20year.-,Nov%202001%E2%80%93%0ADec%202007,-73"},
                        "2009-6-15":{"Name":"2009-2020 Growth",
                                     "Annual Employment Growth (%)": 1.1,
                                     "Annual GDP Growth (%)": 2.3,
                                     "Details":"https://en.wikipedia.org/wiki/List_of_economic_expansions_in_the_United_States#:~:text=the%20early%201980s.-,June%202009%E2%80%93%0AFeb%202020,-128"},
                        "2020-4-30":{"Name":"Post-COVID Growth",
                                     "Annual Employment Growth (%)": "TBD",
                                     "Annual GDP Growth (%)": "TBD",
                                     "Details":"https://en.wikipedia.org/wiki/List_of_economic_expansions_in_the_United_States#:~:text=.%5B18%5D-,April%202020%2D%20Ongoing,-TBD"}}

US_STATE_CODES = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT","Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

colors = [
    'navy', 'darkorange', 'green', 'maroon', 'teal', 'purple', 'olive', 'gray', 'fuchsia', 'lime'
]

def get_period_caption(start_date):
    caption = ""
    for key,value in US_ECON_DETAILS[start_date].items():
        if key == "Details":
            caption = caption + "Link to details: <a>" + str(value) + "</a><br>"
        else:
            caption = caption + key + ": " + str(value) + "<br>"
    return caption

'''
Input: 
    selected_states: a list of strings, a list of states to put on graph
    aqi_metric: a string indicating the metric
    start_date: start date in string
    end_date: end date in string
Output:
    fig: a plotly fig of all curves
'''
def get_general_plot(selected_states, aqi_metric, start_date, end_date):

    # Initialize an empty list of traces
    traces = []

    df = pd.read_csv("data/Integrated AQI-Price.csv")

    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    df['Gas Price'] = df['Gas Price'] * 0.114 # transform from $/Million BTU to $/Gallon

    color_idx = 0
    
    # Loop through the selected states
    for state in selected_states:
        # Get the data for the current state within the selected date range
        # Filter by the selected state
        df_state = df[df['State Name'] == state]

        # Filter by date range
        df_state = df_state[(df_state['Date'] >= start_date) & (df_state['Date'] <= end_date)]

        color1 = colors[color_idx % len(colors)]
        color_idx += 1
        
        # Create a trace for the AQI data of the current state
        traces.append(go.Scatter(
            x=df_state['Date'],
            y=df_state[aqi_metric],
            mode='lines',
            name=f'{aqi_metric}_{state}',
            yaxis='y1',
            line=dict(color=color1, dash = "solid")
        ))

        color2 = colors[color_idx % len(colors)]
        color_idx += 1
        
        # Create a trace for the Gas Price data of the current state
        traces.append(go.Scatter(
            x=df_state['Date'],
            y=df_state['Gas Price'],
            mode='lines',
            name=f'Gas_Price_{state}',
            yaxis='y2',
            line=dict(color=color2, dash='solid', width = 8)
        ))
    
    # Define the layout of the graph
    layout = go.Layout(
        title='Air Quality and Gas Price Trends Comparison',
        xaxis={'title': 'Date'},
        yaxis={'title': 'AQI', 'side': 'left', 'showgrid': False},
        yaxis2={'title': 'Gas Price', 'side': 'right', 'overlaying': 'y', 'showgrid': False},
        hovermode='closest',
        height=750
    )

    shapes = []
    for period in US_RECESSIONS:
        if start_date <= period[0] and period[1] <= end_date:
            shapes.append({
                'type': 'rect',  
                'xref': 'x', 
                'yref': 'paper',
                'x0': period[0],  
                'y0': 0, 
                'x1': period[1],  
                'y1': 1,
                'fillcolor': 'lightblue',  
                'opacity': 0.5,
                'line': {
                    'width': 0,
                },
                'layer': 'below'
            })

            traces.append(go.Scatter(
                x=[(pd.to_datetime(period[0]) + (pd.to_datetime(period[1]) - pd.to_datetime(period[0])) / 2).strftime('%Y-%m-%d')],
                y=[0],  # Y position for the hover text, adjust as needed
                text=[get_period_caption(period[0])],
                mode='markers',
                marker=dict(color='rgba(0,0,0,0)'),
                hoverinfo='text',
                showlegend=False
            ))

    for period in US_RAPID_GROWTH:
        if period[0]>= start_date and period[1]<=end_date:
            shapes.append({
                'type': 'rect',
                'xref': 'x', 
                'yref': 'paper',
                'x0': period[0],  
                'y0': 0, 
                'x1': period[1], 
                'y1': 1,
                'fillcolor': 'orange',  
                'opacity': 0.4,
                'line': {
                    'width': 0,
                },
                'layer': 'below'
            })

            traces.append(go.Scatter(
                x=[(pd.to_datetime(period[0]) + (pd.to_datetime(period[1]) - pd.to_datetime(period[0])) / 2).strftime('%Y-%m-%d')],
                y=[0],  # Y position for the hover text, adjust as needed
                text=[get_period_caption(period[0])],
                mode='markers',
                marker=dict(color='rgba(0,0,0,0)'),
                hoverinfo='text',
                showlegend=False
            ))
        
    
    # Modify the layout to include shapes
    layout['shapes'] = shapes
    
    # Create the figure with the collected traces
    fig = go.Figure(data=traces, layout=layout)
    
    return fig


def get_colormap(aqi_metric, colormap_date):
    df = pd.read_csv("data/Integrated AQI-Price.csv")

    df['State Code'] = df['State Name'].map(US_STATE_CODES)
    merged_data = df[df['Date'] == colormap_date]

    columns_to_keep = ['State Code', aqi_metric, 'Gas Price']
    merged_data = merged_data[columns_to_keep]

    # Define the subplots
    fig_heat = make_subplots(rows=1, cols=2, subplot_titles=(aqi_metric, 'Gas Prices'),
                        specs=[[{"type": "choropleth"}, {"type": "choropleth"}]])

    # Add the AQI choropleth map to the first subplot
    fig_heat.add_trace(
        go.Choropleth(
            locations=merged_data['State Code'],  
            z=merged_data[aqi_metric], 
            locationmode='USA-states', 
            colorscale='Viridis', 
            colorbar_title="Average AQI"
        ),
        row=1, col=1 
    )

    # Add the petroleum prices choropleth map to the second subplot
    fig_heat.add_trace(
        go.Choropleth(
            locations=merged_data['State Code'],
            z=merged_data['Gas Price'],  
            locationmode='USA-states',
            colorscale='Viridis', 
            colorbar_title="Petroleum Prices"
        ),
        row=1, col=2 
    )

    fig_heat.update_layout(
        title_text=f'USA State-level AQI and Gas Prices on {colormap_date}'
    )

    fig_heat.update_geos(
        scope='usa',
        row=1, col=1
    )

    fig_heat.update_geos(
        scope='usa',
        row=1, col=2
    )

    for i in range(len(fig_heat.data)):
        fig_heat.data[i].colorbar.x = 0.5 if i % 2 == 0 else 1

    return fig_heat