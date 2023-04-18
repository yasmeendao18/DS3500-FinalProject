import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# read in data
df = pd.read_csv('household_data.csv')

def make_map():
    filt = df[df['year'] == 2020]
    fig = go.Figure(data=go.Choropleth(
        locations = filt['iso3'],
        z = filt['wat_bas_n'],
        text = filt['country'],
        colorscale = 'Blues',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_ticksuffix = '%',
    ))

    fig.update_layout(
        width=750,
        height=500,
        title_text='2020 Water Coverage Basic Service Percent',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0,
            text='Sources: <a href="https://data.worldbank.org/indicator/NY.GDP.MKTP.PP.CD?end=2021&most_recent_value_desc=true&start=1990&view=chart">\
                GDP World Bank</a>',
            showarrow = False
        )]
    )

    fig.show()

def main():
    make_map()
    
if __name__ == '__main__':
    main()