"""
File: gad.py

Description: A demonstration of our
sankey library using gene-disease associations
"""
import pandas as pd
import sankey as sk


def extract_local_network(gad, phenotype, min_pub=3):
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

    # discard associations with less than <min_pub> publications
    gad = gad[gad.npubs >= min_pub]

    # phenotype of interest
    gad_pheno = gad[gad.phenotype == phenotype]

    # Find all gad associations involving the phenotype-linked genes
    # gad = pd.merge(gad, gad_pheno[['gene']], on='gene')
    gad = gad[gad.gene.isin(gad_pheno.gene)]

    return gad


def main():
    # Read GAD data
    gad = pd.read_csv("gad/gad.csv")

    # Analysis parameters
    phenotype = 'asthma'

    # Filter gad data to identify associations "local" to the specified phenotype
    local = extract_local_network(gad, phenotype, min_pub=3)
    print(local)

    # Generate sankey diagram
    sk.show_sankey(local, 'phenotype', 'gene', vals='npubs')


main()
