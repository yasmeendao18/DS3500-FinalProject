
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

# define the layout

app.layout = html.Div([
    html.H4('Interactive color selection using Dash'),
    html.P("Select color: "),
    dcc.Dropdown(
        id = "dropdown",
        options=['Gold', 'MediumTurquoise', 'LightGreen'],
        value='LightGreen',
        clearable=False
    ),
    dcc.Graph(id="graph"),
    dcc.Graph(id="graph2")

])

# define how the dashboard reacts to control changes



@app.callback(
    Output("graph2", "figure"),
    Input("dropdown", "value")
)
def display_color(color):
    fig = go.Figure(
        data=go.Bar(y=[2, 3, 1],
                    marker_color = color))
    return fig

app.run_server(debug=True)


def main():

    color = 'Red'
    fig = display_color(color)
    fig.show()

# main()