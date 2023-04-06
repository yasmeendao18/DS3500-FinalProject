import pandas as pd
import sankey as sk
from dash import Dash, dcc, html, Input, Output
from collections import Counter


def read_gad():
    """ One-time reading cleaning of gad data to make
    interactive features more responsive """
    gad = pd.read_csv('gad/gad.csv')

    # positive associations only!
    gad = gad[gad.association == 'Y']

    # Focus on phenotype (disease) and gene (symbol) columns only
    gad = gad[['phenotype', 'gene']]

    # Convert phenotype to lowercase
    gad.phenotype = gad.phenotype.str.lower()

    # count publications (rows) for each disease-gene association
    gad = gad.groupby(['phenotype', 'gene']).size().reset_index(name='npubs')

    # sort by gene symbol
    gad.sort_values('npubs', ascending=False, inplace=True)

    return gad

def extract_local_network(gad, phenotype, min_pub=3):

    # discard associations with less than <min_pub> publications
    gad = gad[gad.npubs >= min_pub]

    # phenotype of interest
    gad_pheno = gad[gad.phenotype == phenotype]

    # Find all gad associations involving the phenotype-linked genes
    # gad = pd.merge(gad, gad_pheno[['gene']], on='gene')
    gad = gad[gad.gene.isin(gad_pheno.gene)]

    return gad

# Read the Gad data
gad = read_gad()


# create the layout
app = Dash(__name__)

app.layout = html.Div([
    html.H4('Interactive Gene Disease Association Dashboard'),
    dcc.Graph(id="graph", style={'width': '100vw', 'height': '90vh'}),
    html.P("Select Disease / Phenotype:"),
    dcc.Dropdown(id='phenotype', options=sorted(list(set(gad.phenotype))),
                 value="asthma", clearable=False),
    html.P("Select minimum number of confirming publications:"),
    dcc.Slider(id='min_pubs', min=1, max=10, step=1, value=3),
    html.P("Prune phenotypes connected to only one gene?"),
    dcc.RadioItems(id='prune', options=['Yes', 'No'], value='Yes', inline=True)
])

def prune_local_network(local):
    """ Remove phenotypes that are connected to only one gene """
    counter = Counter(local.phenotype)
    exclude = [k for k,v in counter.items() if v==1]
    local = local[~local.phenotype.isin(exclude)]
    return local


# define the callback
@app.callback(
    Output("graph", "figure"),
    Input("phenotype", "value"),
    Input("min_pubs", "value"),
    Input("prune", "value")
)
def display_sankey(phenotype, min_pubs, prune):
    local = extract_local_network(gad, phenotype, min_pub=min_pubs)

    if prune == 'Yes':
        local = prune_local_network(local)

    # Generate sankey diagram
    fig = sk.make_sankey(local, 'phenotype', 'gene', vals='npubs', line_width=1)

    return fig


# run the server
app.run_server(debug=True)