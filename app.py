# To run the app
# 1. set FLASK_APP=app.py
# 2. flask run

import os
import requests
import json
import numpy as np
from flask import Flask, request, make_response, render_template
from flask_cors import cross_origin
import scrape_and_clean
import plotting_functions

app = Flask(__name__)


@app.route('/', methods=['GET'])
def homepage():

    # Sorry for this mess, this wont run inside the clean method so i had to clean it elsewhere ------------------------
    india_url = 'https://www.mohfw.gov.in/'
    india_df = scrape_and_clean.scrape_table(india_url)
    world_url = 'https://www.worldometers.info/coronavirus/'
    world_df = scrape_and_clean.scrape_table(world_url)

    india_df_clean = scrape_and_clean.clean_data(india_df)
    world_df_clean = scrape_and_clean.clean_data(world_df)
    temp_df = india_df_clean.reset_index()
    temp_df1 = world_df_clean.reset_index()

    # Adding Positive Rate
    # temp_df1['Positive Rate'] = ((temp_df1['TotalCases']/temp_df1['Total Tests'])*100).round(2)
    # temp_df1.replace(np.inf, 0, inplace=True)

    temp_df.rename(columns={temp_df.columns[1]: 'Total Cases',
                            temp_df.columns[3]: 'Deaths',
                            temp_df.columns[2]: 'Total Recovered'},
                   inplace=True)
    response = requests.get("https://api.covid19india.org/state_test_data.json")
    data = json.loads(response.text)
    data1 = data.get('states_tested_data')
    temp_df['ICU Beds'] = 0
    temp_df['Isolation Beds'] = 0
    temp_df['Total Tests'] = 0
    temp_df['Test positive rate'] = 0
    for x in data1:
        if x.get('state') in temp_df[temp_df.columns[0]].values:
            if x.get('testpositivityrate') != '':
                temp_df.loc[temp_df[temp_df.columns[0]] == x.get('state'), 'Test positive rate'] = float(
                    x.get('testpositivityrate')[:-1])
            if x.get('totaltested') != '':
                temp_df.loc[temp_df[temp_df.columns[0]] == x.get('state'), 'Total Tests'] = float(x.get('totaltested'))
            if x.get('numicubeds') != '':
                temp_df.loc[temp_df[temp_df.columns[0]] == x.get('state'), 'ICU Beds'] = int(x.get('numicubeds'))
            if x.get('numisolationbeds') != '':
                temp_df.loc[temp_df[temp_df.columns[0]] == x.get('state'), 'Isolation Beds'] = int(
                    x.get('numisolationbeds'))

    # The cleaning is now done -----------------------------------------------------------------------------------------

    total = temp_df[['Total Cases', 'Total Recovered', 'Deaths']].sum().values
    outcome = sum(temp_df[['Total Recovered', 'Deaths']].sum())
    cases = temp_df['Total Cases'].sum()
    total = np.append(total, cases - outcome)

    total1 = temp_df1.loc[0][[1,5,3,6]].values

    total_cases_india = temp_df.columns[1]
    total_recovered_india = temp_df.columns[2]
    deaths_india = temp_df.columns[3]
    total_tests_india = temp_df.columns[7]
    positive_rate_india = temp_df.columns[8]

    total_cases_world = temp_df1.columns[1]
    total_recovered_world = temp_df1.columns[5]
    deaths_world = temp_df1.columns[3]
    total_tests_world = temp_df1.columns[7]
    positive_rate_world = temp_df1.columns[9]

    confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
                    '/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv '
    confirmed_df = scrape_and_clean.scrape_and_clean_time_series(confirmed_url)
    deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
                 '/csse_covid_19_time_series/time_series_covid19_deaths_global.csv '
    deaths_df = scrape_and_clean.scrape_and_clean_time_series(deaths_url)
    recovered_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
                    '/csse_covid_19_time_series/time_series_covid19_recovered_global.csv '
    recovered_df = scrape_and_clean.scrape_and_clean_time_series(recovered_url)

    return render_template('index.html',
                           total_data=total,
                           total_data1=total1,
                           table_in_plotly=plotting_functions.table(temp_df),
                           table_in_plotly1=plotting_functions.table(temp_df1),
                           total_cases_deaths=plotting_functions.bar_chart(temp_df, total_cases_india,
                                                                           deaths_india, 'India'),
                           total_cases_deaths1=plotting_functions.bar_chart(temp_df1.iloc[2:22, :], total_cases_world,
                                                                            deaths_world, 'World'),
                           pie_total_cases_deaths=plotting_functions.pie_chart(temp_df, total_cases_india,
                                                                               deaths_india, 'India'),
                           pie_total_cases_deaths1=plotting_functions.pie_chart(temp_df1.iloc[1:22, :],
                                                                                total_cases_world,
                                                                                deaths_world, 'World'),
                           total_recovered_cases=plotting_functions.bar_chart(temp_df, total_recovered_india,
                                                                              total_cases_india, 'India'),
                           total_recovered_cases1=plotting_functions.bar_chart(temp_df1.iloc[2:22, :],
                                                                               total_recovered_world,
                                                                               total_cases_world, 'World'),
                           test_positive_rate_tests=plotting_functions.bar_chart(temp_df, positive_rate_india,
                                                                                 total_tests_india, 'India'),
                           test_positive_rate_tests1=plotting_functions.bar_chart(temp_df1.iloc[2:22, :],
                                                                                  positive_rate_world,
                                                                                  total_tests_world, 'World'),
                           time_series=plotting_functions.time_series(confirmed_df, deaths_df, recovered_df),)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Starting app on port {port}")
    app.run(debug=False, port=port, host='127.0.0.1')
