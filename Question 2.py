# Question 2
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NBA using 2018 data.

import pandas as pd
import numpy as np
import scipy.stats as stats



def team_nba(team):
    return team.split()[-1]


def city_nba(j):
    for i in nba_city.index.values:
        if j in i:
            town = nba_city.loc[i]
            return town[0]


nba_df = pd.read_csv("nba.csv")
cities = pd.read_html("wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]

nba_df = nba_df.where(nba_df['year'] == 2018).dropna()
nba_df['team'] = nba_df['team'].replace('\*', '', regex=True).replace('\(\d*\)', '', regex=True)
nba_city = cities[['Metropolitan area', 'NBA']].replace('\[\w+\s\d*\]', '', regex=True).set_index('NBA')
cities = cities[['Metropolitan area', 'Population (2016 est.)[8]']].replace('\[\w+\s\d*\]', '', regex=True).replace('—',
                                                                                                                    '',
                                                                                                                    regex=True).set_index(
    'Metropolitan area')


def nba_correlation():
    # YOUR CODE HERE
    #     raise NotImplementedError()
    nba_df = pd.read_csv("nba.csv")
    cities = pd.read_html("wikipedia_data.html")[1]
    cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]

    nba_df = nba_df.where(nba_df['year'] == 2018).dropna()
    nba_df['team'] = nba_df['team'].replace('\*', '', regex=True).replace('\(\d*\)', '', regex=True)
    nba_city = cities[['Metropolitan area', 'NBA']].replace('\[\w+\s\d*\]', '', regex=True).set_index('NBA')
    cities = cities[['Metropolitan area', 'Population (2016 est.)[8]']].replace('\[\w+\s\d*\]', '', regex=True).replace(
        '—', '', regex=True).set_index('Metropolitan area')
    nba_df['city'] = nba_df['team'].apply(lambda x: team_nba(x))
    nba_df['city'] = nba_df['city'].apply(lambda x: city_nba(x))
    list_dict = []
    for group, frame in nba_df.groupby('city'):
        win = np.sum(frame['W'].astype(int))
        all = np.sum(frame['L'].astype(int)) + np.sum(frame['W'].astype(int))
        ratio = win / all
        ratio_dict = {'City': group, 'Ratio': ratio}
        list_dict.append(ratio_dict)

    last_df = pd.DataFrame(list_dict).set_index('City')
    last_df = pd.merge(last_df, cities, how='inner', left_index=True, right_index=True)
    # last_df
    win_loss_by_region = list(last_df['Ratio'])
    population_by_region = list(last_df['Population (2016 est.)[8]'].astype(float))
    assert len(population_by_region) == len(win_loss_by_region)  # "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28  # "Q2: There should be 28 teams being analysed for NBA"
    cor = stats.pearsonr(win_loss_by_region, population_by_region)

    return stats.pearsonr(population_by_region, win_loss_by_region)


print(nba_correlation())
