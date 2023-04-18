import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df_household = pd.read_csv('household_data.csv')
df_household = df_household.set_index('year')
country_list = list(df_household.country.unique())

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='Country',
        options=[{'label': i, 'value': i} for i in country_list],
        value=country_list[0]
    ),
    dcc.Dropdown(
        id='Service',
        options=[{'label': i, 'value': i} for i in ['wat', 'san', 'hyg']],
        value='wat'
    ),
    dcc.Dropdown(
        id='Service_Residence',
        options=[{'label': i, 'value': i} for i in ['Service Level', 'Residence Type']],
        value='Service Level'
    ),
    dcc.Dropdown(
        id='Service_level',
        options=[{'label': i, 'value': i} for i in ['bas', 'lim', 'unimp', 'sur', 'sm', 'premises', 'available',
                                                    'quality', 'pip', 'npip', 'od', 'sdo_sm', 'fst_sm', 'sew_sm',
                                                    'lat', 'sep', 'sew', 'nfac']],
        value='Select service level'
    ),
    dcc.Dropdown(
        id='Residence_type',
        options=[{'label': i, 'value': i} for i in ['_n', '_u', '_r']],
        value='Total'
    ),
    dcc.Graph(
        id='my-graph'
    )
])


@app.callback(
    Output('my-graph', 'figure'),
    [Input('Country', 'value'),
     Input('Service', 'value'),
     Input('Service_Residence', 'value'),
     Input('Service_level', 'value'),
     Input('Residence_type', 'value')])
def update_graph(selected_value_1, selected_value_2, selected_value_3, selected_value_4, selected_value_5):
    filtered_data = df_household[(df_household['country'] == selected_value_1)]
    service_data = filtered_data.filter(like=str(selected_value_2))
    if selected_value_3 == 'Service Level':
        df_level = service_data.filter(like=str(selected_value_4))
        fig = px.line(df_level, y=df_level.columns)
    elif selected_value_3 == 'Residence Type':
        df_residence = service_data.filter(like=str(selected_value_5))
        fig = px.line(df_residence, y=df_residence.columns)
    # & (df_household['column-2'] == selected_value_2)]
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
