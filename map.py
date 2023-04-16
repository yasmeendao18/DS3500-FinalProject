import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import folium
import geopandas


def read_data():
    df_county = pd.read_csv('wash-country-2020.csv')
    df_county.drop(['Year'], axis=1, inplace=True)
    return df_county

def make_map():
    # The data is in the first table - this changes from time to time - wikipedia is updated all the time.
    
    # Read the geopandas dataset
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    
    # Merge the two DataFrames together
    table = world.merge(table, how="left", left_on=['name'], right_on=['Country'])
    
    # Clean data: remove rows with no data
    table = table.dropna(subset=['kg/person (2002)[9][note 1]'])
    
    # Create a map
    my_map = folium.Map()
    
    # Add the data
    folium.Choropleth(
        geo_data=table,
        name='choropleth',
        data=table,
        columns=['Country', 'kg/person (2002)[9][note 1]'],
        key_on='feature.properties.name',
        fill_color='OrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Meat consumption in kg/person'
    ).add_to(my_map)
    my_map.show()

def main():
    print('Reading data...')
    
if __name__ == '__main__':
    main()