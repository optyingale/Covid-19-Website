import requests
import pandas as pd
import numpy as np
import re
import json
from bs4 import BeautifulSoup


def scrape_table(url):
    # Creating soup for each source
    soup = BeautifulSoup(requests.get(url).content, 'html5lib')

    # Getting rows for each table from soup
    table_rows = soup.find_all('tr')

    # Getting column names given as the 'th' tag; strip=True means that the tags are removed from the string
    column_names = []
    for cell in table_rows[0].find_all('th'):
        column_names.append(cell.get_text(strip=True))

    # Getting cell data in list to later create a DataFrame
    each_row = []
    for row in table_rows[1:]:
        each_row.append([cell.get_text(strip=True) for cell in row.find_all('td')])

    # Creating DataFrame from extracted data
    df = pd.DataFrame(each_row, columns=column_names)

    return df


def clean_data(df):
    # Checking for which dataframe is recieved
    if 'Name of State / UT' in df:
        df = df.iloc[:35, :]
        df.drop('S. No.', axis=1, inplace=True)
        df.set_index('Name of State / UT', inplace=True)
        for col in df.columns:
            df[col] = df[col].str.extract('(\d+)').astype(int)
        df.sort_values(df.columns[0], ascending=False, inplace=True)

        # Creating recovery_rate to understand more about the closed cases
        df['recovery_rate (in percentage)'] = (
                    (df[df.columns[1]] / (df[df.columns[1]] + df[df.columns[2]])) * 100).round(2)

        # No idea why this isnt working
    #        df.rename(columns={df.columns[1]:'Total Cases',
    #                        df.columns[3]:'Deaths',
    #                        df.columns[2]:'Total Recovered'},
    #                  inplace=True)
#        response = requests.get("https://api.covid19india.org/state_test_data.json")
#        data = json.loads(response.text)
#        data1 = data.get('states_tested_data')
#        df['ICU Beds'] = 0
#        df['Isolation Beds'] = 0
#        df['Total Tests'] = np.zeros((df.shape[0], 1))
#        df['Test positive rate'] = 0
#        for x in data1:
#            if x.get('state') in df[df.columns[0]].values:
#                if x.get('testpositivityrate') != '':
#                    df.loc[df[df.columns[0]]==x.get('state'),
#                           'Test positive rate'] = float(x.get('testpositivityrate')[:-1])
#                if x.get('totaltested') != '':
#                    df.loc[df[df.columns[0]]==x.get('state'), 'Total Tests'] = float(x.get('totaltested'))
#                if x.get('numicubeds') != '':
#                    df.loc[temp_df[df.columns[0]]==x.get('state'), 'ICU Beds'] = int(x.get('numicubeds'))
#                if x.get('numisolationbeds') != '':
#                    df.loc[temp_df[df.columns[0]]==x.get('state'),
#                    'Isolation Beds'] = int(x.get('numisolationbeds'))

    elif 'TotalDeaths' in df:
        # The reason for not hard coding here below is that
        # The website might add on later new countires whose data might not be available now
        world_df = df
        upper_index = world_df[world_df['Country,Other'] == 'World'].index[0]
        lower_index = world_df[world_df['Country,Other'] == 'Total:'].index[0]

        # 15 May, website updated their table and added a number column
        world_df.drop('#', axis=1, inplace=True)

        # Dropping columns after active cases, this can be changed depending on need for analysis later on
        df = world_df.iloc[upper_index:lower_index, :-10]
        df['Total Tests'] = world_df.loc[:, 'TotalTests'].iloc[upper_index:lower_index]
        df.set_index('Country,Other', inplace=True)

        # Converting alphanumeric data to pure numeric and later to integer type
        # this works for all values
        for col in df.columns:
            df[col] = [''.join(re.findall(r'\d+', df[col].values[i])) for i in range(len(df[col]))]
            df[col] = df[col].replace('', 0)
            df[col] = df[col].apply(int)

        df.sort_values('TotalCases', ascending=False, inplace=True)
        df['recovery_rate (in percentage)'] = (
                    (df[df.columns[4]] / (df[df.columns[4]] + df[df.columns[2]])) * 100).round(2)
        df['Positive Rate'] = ((df['TotalCases'] / df['Total Tests']) * 100).round(2)
        df['Positive Rate'].replace(np.inf, 0, inplace=True)

    return df


def scrape_and_clean_time_series(url):
    df = pd.read_csv(url)
    df = df[df['Country/Region'] == 'India'].iloc[:, 4:].T.reset_index()
    df['Date'] = pd.DatetimeIndex(df['index'])
    df.rename(columns={df.columns[1]: 'India'}, inplace=True)
    df.drop('index', axis=1, inplace=True)
    return df
