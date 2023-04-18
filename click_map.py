import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Load the data
data = pd.read_csv("household_data.csv")

# create sub dataframes filtered by column
issue = {
    'water': (data.filter(regex='.*wat.*|iso3|year|country', axis=1), 'Water', 'Blues'),
    'sanitation': (data.filter(regex='.*san.*|iso3|year|country', axis=1), 'Sanitation', 'Purples'),
    'hygiene': (data.filter(regex='.*hyg.*|iso3|year|country', axis=1), 'Hygiene', 'RedOr'),
    'gdp': (data.filter(regex='gdp|iso3|year|country', axis=1), 'GDP', 'Greens')
}

# Create the map figure
map_fig = px.choropleth(
    data_frame=data,
    locations="iso3",
    color="wat_bas_n",
    hover_name="country",
    projection="natural earth",
    title="World Water Coverage by Country",
    color_continuous_scale='Blues',
    scope='world',
    height=500,
)

# Create the line chart figure
line_fig = go.Figure()

# Define the app
app = Dash(external_stylesheets=[dbc.themes.LUX])

# Define the app layout
app.layout = dbc.Container(
    html.Div([
    html.H1("Where's my Water?"),
    html.P('Chose an issue:'),
    dcc.Dropdown(
        id='drop',
        options=[
            {'label': 'Water Coverage', 'value': 'water'},
            {'label': 'Sanitation Coverage', 'value': 'sanitation'},
            {'label': 'Hygiene Coverage', 'value': 'hygiene'},
            {'label': 'Gross Domestic Product (GDP)', 'value': 'gdp'}
        ],
        value = 'water',
    ),
    html.Hr(),
    dcc.Graph(
        id="map",
        figure=map_fig,
        clickData={"points": [{"location": "USA"}]},
        config={'displayModeBar': False}
    ),
    dcc.Graph(
        id="line",
        figure=line_fig
    ),
    html.Div([
        html.P('Sources:'),
        html.Ul(children=[
        html.Li(html.A('WHO/UNICEF (JMP) WASH Data', href='https://washdata.org/data')),
        html.Li(html.A('For GDP', href='https://data.worldbank.org/indicator/NY.GDP.MKTP.PP.CD?end=2021&most_recent_value_desc=true&start=1990&view=chart')),
        ])
    ]
    )
]))

@app.callback(
    Output('map', 'figure'),
    Input('drop', 'value')
)
# Define the app callback for the map
def make_map(value):
    """ creates a map of 2020 with the inputted dataframe

        parameters:
            value (string): the current issue selected in the dropdown

        returns:
            fig (plot): map of world

    """
    params = issue[value]
    issue_df = params[0]
    title = params[1]
    colors = params[2]
    val = issue_df.columns[3]
    fig = px.choropleth(
        data_frame=issue_df,
        locations="iso3",
        color=val,
        hover_name="country",
        projection="natural earth",
        title=f"World {title} Coverage by Country",
        color_continuous_scale=colors,
        scope="world",
        height=500,
        labels={val: f'{title} Cov.%',
                'iso3': 'Country Code'}
    )
    return fig


# Define the app callback for line chart
@app.callback(
    Output("line", "figure"),
    [
        Input("map", "clickData"),
        Input("drop", "value")
    ]
)
def update_line_chart(click_data, value):
    ''' Update the line chart based on the map click
        and current issue selected in the dropdown
        
        Parameters.
            click_data (dict): The click data from the map
            value (string): The current issue selected in the dropdown
            
        Returns.
            line_fig (plot): line chart of the selected issue
    '''
    selected = issue[value]
    issue_df = selected[0]
    title = selected[1]
    if click_data:
        location = click_data["points"][0]["location"]
        filtered_df = issue_df[issue_df["iso3"] == location]
        line_fig = px.line(
            filtered_df,
            x="year",
            y=filtered_df.columns[3:],
        )
        line_fig.update_layout(
            xaxis_title="Year",
        )
        if value != 'gdp':
            line_fig.update_layout(
                title=f"{title} Coverages for {location}",
                yaxis_title=f"{title} Coverage (%)",
                yaxis_range=[0, 100],
            )
        else:
            line_fig.update_layout(
                title=f"{title} for {location}",
            )
    else:
        line_fig = go.Figure()

    return line_fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
