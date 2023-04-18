'''

Clean the data from the JMP_2021_WLD.xlsx file and gdp data from the API_NY.GDP.MKTP.CD_DS2_en_csv_v2_5358352.csv file
returns a csv file with the cleaned data

'''
import pandas as pd

def _read_sheet(sheet, first):
    ''' Read a sheet from the JMP_2021_WLD.xlsx file and return a dataframe
    args.
        sheet: str, name of the sheet to read
        first: bool, whether this is the first sheet to be read
    returns.
        df: pd.DataFrame, the dataframe of the sheet
    '''
    # clean the dataframe of necessary columns
    df = pd.read_excel('base_data/JMP_2021_WLD.xlsx', sheet_name=sheet)\
        .drop(columns=['sl','region_who','region_unicef_programme','region_unicef_reporting'], axis=1)\
        .rename({'name': 'country', 'pop_n': 'pop', 'prop_u': 'pop_urban', 'region_sdg': 'region'}, axis=1)\
        .dropna(subset=['country'])\
        .set_index(['country', 'iso3', 'region', 'year'])
    df = df.loc[:,~df.columns.str.startswith('arc')]
    if not first:
        df = df.drop(columns=['pop', 'pop_urban'], axis=1)
    return df

def build_pop_df():
    ''' Read the JMP_2021_WLD.xlsx file and return a dataframe with population and urban population
    returns.
        pop_df: pd.DataFrame, the dataframe of the JMP_2021_WLD.xlsx file
    '''
    # read the data
    wat = _read_sheet('wat', first=True)
    hyg = _read_sheet('hyg', first=False)
    san = _read_sheet('san', first=False)
    
    # combine the dataframes
    comb_df = pd.concat([wat, hyg, san], axis=1, join='inner')
    
    # make a copy of the dataframe
    pop_df = comb_df.copy()
    
    # get original population value
    pop_df['pop'] = comb_df['pop'] * 1000
    return pop_df

def build_gdp_df():
    ''' Read the API_NY.GDP.MKTP.CD_DS2_en_csv_v2_5358352.csv file and return a dataframe with gdp
    returns.
        gdp: pd.DataFrame, the dataframe
    '''
    gdp = pd.read_csv('base_data/API_NY.GDP.MKTP.CD_DS2_en_csv_v2_5358352.csv', header=2)\
        .rename({'Country Code': 'iso3'}, axis=1)\
        .drop(columns=['Country Name', 'Indicator Name', 'Indicator Code', 'Unnamed: 66'], axis=1)
    gdp = pd.melt(gdp, id_vars=['iso3'], var_name='year', value_name='gdp')
    gdp.year = gdp.year.astype('float64')
    gdp = gdp.set_index(['iso3', 'year'])
    return gdp


def main():
    pop_df = build_pop_df()
    gdp = build_gdp_df()
    all = pop_df.join(gdp, on=['iso3', 'year'], how='left')
    all.to_csv('household_data.csv')
    
if __name__ == '__main__':
    main()