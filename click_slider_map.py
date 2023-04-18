import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from millify import millify


def try_millify(x, precision):
    ''' Try to millify a number, if it fails return the number
    args.
        x: number to millify
        precision: number of decimal places to round to
    returns.
        millified number or original number
    '''
    try:
        return millify(x, precision)
    except:
        return x


# Load the data
data = pd.read_csv("household_data.csv")

# create sub dataframes filtered by column with titles anc colors
issue = {
    'water': (data.filter(regex='.*wat.*|iso3|year|country', axis=1), 'Water', 'Blues'),
    'sanitation': (data.filter(regex='.*san.*|iso3|year|country', axis=1), 'Sanitation', 'Purples'),
    'hygiene': (data.filter(regex='.*hyg.*|iso3|year|country', axis=1), 'Hygiene', 'RedOr'),
    'gdp': (data.filter(regex='gdp|iso3|year|country', axis=1), 'GDP', 'Greens')
}

# dictionary of column names by service
services = {
    'baseline': ['bas', 'lim', 'unimp', 'sur', 'nfac', 'od'],
    'available': ['sm', 'premises', 'available', 'quality', 'sdo_sm', 'fst_sm', 'sew_sm'],
    'infrastructure': ['pip', 'npip', 'lat', 'sep', 'sew'],
}

# remap service level names to more readable names
service_map = {
    'bas': 'Basic',
    'lim': 'Limited',
    'unimp': 'Unimproved',
    'sur': 'Surface water',
    'nfac': 'No facility',
    'od': 'Open defecation',
    'sm': 'Safe management',
    'premises': 'On premises',
    'available': 'Available when needed',
    'quality': 'Free from contamination',
    'sdo_sm': 'Disposed of',
    'fst_sm': 'Emptied and treated',
    'sew': 'Sewerage system',
    'sew_sm': 'Waste water treated',
    'pip': 'Piped',
    'npip': 'Non-piped',
    'lat': 'Latrine',
    'sep': 'Septic tank',
}

# dict for slider labels
year_dict = {}
for i in range(2000, 2020, 1):
    year_dict[i] = str(i)

# create dropdown options for filters
drop_ops = {
    'Service Level': [{'label': 'Availability', 'value': 'baseline'},
                      {'label': 'Safe Management', 'value': 'available'},
                      {'label': 'Infrastructure', 'value': 'infrastructure'}],
    'Residence Type': [{'label': 'National', 'value': '_n'},
                       {'label': 'Urban', 'value': '_u'},
                       {'label': 'Rural', 'value': '_r'}],
}

# define styling
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "0rem 1rem",
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
    height=400,
)

# Create the line chart figure
line_fig = go.Figure()

# Define the app
app = Dash(external_stylesheets=[dbc.themes.LUX])

# define sidebar with filters
sidebar = html.Div([
    html.H1("Water We Doing?"),
    html.P(
        "a dashboard to visualize water supply, sanitation, and hygiene coverage as well as country GDP around the world with data from WHO/UNICEF Joint Monitoring Program and World Bank",
        style={'font-size': '13px'}),
    html.H5('Choose an issue:'),
    dcc.Dropdown(
        id='issue',
        options=[
            {'label': 'Water Coverage', 'value': 'water'},
            {'label': 'Sanitation Coverage', 'value': 'sanitation'},
            {'label': 'Hygiene Coverage', 'value': 'hygiene'},
            {'label': 'Gross Domestic Product (GDP)', 'value': 'gdp'}
        ],
        value='water'
    ),
    html.Div([
        html.Hr(),
        html.H5('Filter by:'),
        html.P('Service Level:'),
        dcc.Dropdown(
            id='service_level',
            options=drop_ops['Service Level'],
            value='baseline'
        ),
        html.Br(),
        html.P('Residence Type:'),
        dcc.Dropdown(
            id='residence_type',
            options=drop_ops['Residence Type'],
            value='_n'
        ), ]
    ),
    html.Div([
        html.Hr(),
        html.P('built by: Yasmeen Dao, Emma Shek, Lilian Uong, Yidi Wang, Felix Yang, Sabrina Zhou'),
        html.Hr(),
        html.P('Sources:'),
        html.Ul(children=[
            html.Li(html.A('WHO/UNICEF WASH Data', href='https://washdata.org/data')),
            html.Li(html.A('For GDP',
                           href='https://data.worldbank.org/indicator/NY.GDP.MKTP.PP.CD?end=2021&most_recent_value_desc=true&start=1990&view=chart')),
        ])
    ], className='fixed-bottom', style={"width": "20rem", "padding": "1rem 1rem", "z-index": "-100"}),
], style=SIDEBAR_STYLE)

# define main content with map and line chart
content = html.Div([
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
    html.P('Chose year range:'),
    dcc.RangeSlider(id='year-range-slider', min=2000, max=2020, step=1, value=[2005, 2015],
                    marks=year_dict)
], style=CONTENT_STYLE)

# Define the app layout
app.layout = dbc.Container([sidebar, content], fluid=True)


@app.callback(
    Output('map', 'figure'),
    Input('issue', 'value')
)
# Define the app callback for the map
def make_map(value):
    """ creates a map of 2020 with the inputted dataframe

        parameters:
            value (string): the current issue selected in the dropdown

        returns:
            fig (plot): map of world

    """
    # parse value to get the correct tuple
    params = issue[value]
    issue_df = params[0].copy()
    title = params[1]
    colors = params[2]

    # format the display data
    val = issue_df.columns[3]
    issue_df[f'{val} '] = issue_df[val].map(lambda x: try_millify(x, precision=5))

    # log scale for GDP and format the display data
    if val == 'gdp':
        issue_df[val] = issue_df[val].map(lambda x: np.log10(x))
    context = 'Cov.%' if value != 'gdp' else '$'

    # make the map
    fig = px.choropleth(
        data_frame=issue_df,
        locations="iso3",
        color=val,
        hover_name="country",
        projection="natural earth",
        color_continuous_scale=colors,
        scope="world",
        height=400,
        labels={val: f'{title} {context}',
                'iso3': 'Country Code'},
        custom_data=['country', val, f'{val} ', 'iso3']
    )

    # set margins and title
    fig.update_layout(
        margin=dict(l=30, r=30, t=60, b=0),
        title=dict(text=f"<b>World {title} Coverage Map</b>", font=dict(size=24), yref='paper'),
        title_x=0.5,
    )

    # gdp specific formatting
    if value == 'gdp':
        fig.update_layout(
            coloraxis_colorbar=dict(
                title=f'{title} {context}',
                x=1,
                tickvals=[8, 9, 10, 11, 12, 13],
                ticktext=['100M', '1B', '10B', '100B', '1T', '10T']),
        )
        fig.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>' + 'Country Code: %{customdata[3]}<br>' + f'{title} {context}:' + '%{customdata[2]}'
        )
    return fig


# Define the app callback for line chart
@app.callback(
    Output("line", "figure"),
    [
        Input("map", "clickData"),
        Input("issue", "value"),
        Input("service_level", "value"),
        Input("residence_type", "value"),
        Input('year-range-slider', 'value')
    ]
)


def update_line_chart(click_data, iss, ser_lev, res_type, year_input):
    ''' Update the line chart based on the map click
        and current issue selected in the dropdown

        Parameters.
            click_data (dict): The click data from the map
            iss (string): The current issue selected in the dropdown
            ser_lev (string): The current service level selected in the dropdown
            res_type (string): The current residence type selected in the dropdown
            year_inp (list): range of years to display on graph

        Returns.
            line_fig (plot): line chart of the selected issue
    '''
    # break up the issue dictionary
    selected = issue[iss]
    line_df = selected[0].copy()
    title = selected[1]

    # break up the service level dictionary
    serv = services[ser_lev]
    if iss != 'gdp':
        fil_cols = ['iso3', 'year', 'country'] + [col for col in line_df.columns if
                                                  any([x in col for x in serv]) and col.endswith(res_type)]
        line_df = line_df[fil_cols]

    # get the data for the selected country
    if click_data:
        location = click_data["points"][0]["location"]
        filtered_df = line_df[line_df["iso3"] == location]
        new_dict = {string: service_map[key] for string in filtered_df.columns for key in service_map.keys() if
                    key in string}
        filtered_df = filtered_df.rename(columns=new_dict)

        # assign sun years to be greater than or = min val and less than or = max val
        filtered_df = filtered_df[(filtered_df['year'] >= year_input[0]) & (filtered_df['year'] <= year_input[1])]

        # build the line chart
        line_fig = px.line(
            filtered_df,
            x="year",
            y=filtered_df.columns[3:],
            height=400,
        )

        # format the line chart
        line_fig.update_layout(
            title=f"<b>{filtered_df['country'].iloc[0]} -- Year by Year</b>",
            title_x=0.5,
            margin=dict(l=30, r=30, t=60, b=0),
            xaxis_title="Year",
        )
        line_fig.for_each_trace(
            lambda trace: trace.update(visible='legendonly') if trace.name != filtered_df.columns[3] else ())

        # gdp specific formatting
        if iss != 'gdp':
            line_fig.update_layout(
                yaxis_title=f"{title} Coverage (%)",
            )

    else:
        line_fig = go.Figure()

    return line_fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
