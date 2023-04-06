
"""
Sabrina Zhou
DS3500 / Dash
Sun Dash / Homework 2
1/6/23 / 1/10/23
"""

import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import base64

image_path = 'sunpic.jpeg'


# Using base64 encoding and decoding https://community.plotly.com/t/how-to-embed-images-into-a-dash-app/61839
def b64_image(image_filename):
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

def read_sun():
    """
    One-time reading cleaning of sun data to make
    interactive features more responsive
    """
    # read csv separated by semicolon
    sun = pd.read_csv('sun.csv', sep=';')

    # dataframe only with decimal year and number of sunspots
    sun = sun.iloc[:, [2, 3]]
    sun.columns = ['Time (years)', 'Sunspot Number']
    return sun


# read the sun data
sun = read_sun()

# create the layout
app = Dash(__name__)

# dict for slider labels
year_dict = {}
for i in range(1740, 2040, 10):
    year_dict[i] = str(i)

app.layout = html.Div([
    html.H1('Interactive Sunspot Dashboard'),
    dcc.Graph(id='sunspot-graph', style={'width': '80w', 'height': '70vh'}),
    html.P('Chose year range:'),
    dcc.RangeSlider(id='year-range-slider', min=1749, max=2023, step=20, value=[1800, 1900],
                    marks=year_dict),
    html.P('Chose number of observation periods for smoothing:'),
    dcc.Slider(id='running-slider', min=1, max=12, step=1, value=6,),
    html.H1('Interactive Sunspot Cycle Dash'),
    dcc.Graph(id="sunspot-var-graph", style={'width': '80vw', 'height': '70vh'}),
    html.P('Tune cycle period'),
    dcc.Slider(id='tune-slider', min=0, max=12, step=1, value=11),
    html.H2('NASA Current Sun Image:'),
    html.Img(src=b64_image(image_path), style={'width': '20vw', 'height': '40vh'})
])


# define the callback
@app.callback(
    Output('sunspot-graph', 'figure'),
    Input('year-range-slider', 'value'),
    Input('running-slider', 'value')
)
def make_line(year_inp, smooth_val):
    """creates a line graph of number of sunspots over a specified time range and a smoothed data line

            parameters:
                year_inp (list): range of years to display on graph
                smooth_val (int): length of observation period to smooth data

            returns:
                line_fig (plot): line plot that displays user inputted range of years and smoothed data

    """
    # assign sun years to be greater than or = min val and less than or = max val
    sun_years = sun[(sun['Time (years)'] >= year_inp[0]) & (sun['Time (years)'] <= year_inp[1])]
    # calc moving average of df https://www.geeksforgeeks.org/how-to-calculate-moving-average-in-a-pandas-dataframe/
    sun['running'] = sun['Sunspot Number'].rolling(smooth_val).mean()
    line_fig = px.line(sun_years,
                       x='Time (years)', y=['Sunspot Number', 'running'],
                       title='International sunspot number Sn: monthly mean and 13-month smoothed number')

    return line_fig


# define the callback
@app.callback(
    Output("sunspot-var-graph", "figure"),
    Input("tune-slider", "value"),
)
def make_scatter(value):
    """creates a scatter plot to visualize variability of sunspot cycle

            parameters:
                value (int): determines tune cycle

            returns:
                scatter_fig (plot): scatter plot of sunspot cycle

    """
    sun_mod = sun
    # create new column 'Years' that is the modulo of the value inputted by the user
    sun_mod['Years'] = sun_mod['Time (years)'].mod(value)
    scatter_fig = px.scatter(sun_mod,
                             x='Years', y='Sunspot Number',
                             title=f'Sunspot Cycle: {value}')

    return scatter_fig


# run the server
app.run_server(debug=True)
