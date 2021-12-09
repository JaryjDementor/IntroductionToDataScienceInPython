# Description
# In this assignment you must read in a file of metropolitan regions and associated sports teams from assets/wikipedia_data.html and answer some questions about each metropolitan region. Each of these regions may have one or more teams from the "Big 4": NFL (football, in assets/nfl.csv), MLB (baseball, in assets/mlb.csv), NBA (basketball, in assets/nba.csv or NHL (hockey, in assets/nhl.csv). Please keep in mind that all questions are from the perspective of the metropolitan region, and that this file is the "source of authority" for the location of a given sports team. Thus teams which are commonly known by a different area (e.g. "Oakland Raiders") need to be mapped into the metropolitan region given (e.g. San Francisco Bay Area). This will require some human data understanding outside of the data you've been given (e.g. you will have to hand-code some names, and might need to google to find out where teams are)!
#
# For each sport I would like you to answer the question: what is the win/loss ratio's correlation with the population of the city it is in? Win/Loss ratio refers to the number of wins over the number of wins plus the number of losses. Remember that to calculate the correlation with pearsonr, so you are going to send in two ordered lists of values, the populations from the wikipedia_data.html file and the win/loss ratio for a given sport in the same order. Average the win/loss ratios for those cities which have multiple teams of a single sport. Each sport is worth an equal amount in this assignment (20%*4=80%) of the grade for this assignment. You should only use data from year 2018 for your analysis -- this is important!
#
# Notes
# Do not include data about the MLS or CFL in any of the work you are doing, we're only interested in the Big 4 in this assignment.
# I highly suggest that you first tackle the four correlation questions in order, as they are all similar and worth the majority of grades for this assignment. This is by design!
# It's fair game to talk with peers about high level strategy as well as the relationship between metropolitan areas and sports teams. However, do not post code solving aspects of the assignment (including such as dictionaries mapping areas to teams, or regexes which will clean up names).
# There may be more teams than the assert statements test, remember to collapse multiple teams in one city into a single value!

# Question 1
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NHL using 2018 data.

import pandas as pd
import numpy as np
import scipy.stats as stats
import re


def team_nhl(team):
    return team.split()[-1]


def city_nhl(j):
    for i in nhl_city.index.values:
        if j in i:
            town = nhl_city.loc[i]
            return town[0]


nhl_df = pd.read_csv(r"nhl.csv")
cities = pd.read_html(r"wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
nhl_df = nhl_df.where(nhl_df['year'] == 2018).dropna()
nhl_df['team'] = nhl_df['team'].replace('\*', '', regex=True)
nhl_city = cities[['Metropolitan area', 'NHL']].replace('\[\w+\s\d*\]', '', regex=True).set_index('NHL')
cities = cities[['Metropolitan area', 'Population (2016 est.)[8]']].replace('\[\w+\s\d*\]', '', regex=True).replace('—','',regex=True).set_index('Metropolitan area')


def nhl_correlation():
    # YOUR CODE HERE
    nhl_df['city'] = nhl_df['team'].apply(lambda x: team_nhl(x))
    nhl_df['city'] = nhl_df['city'].apply(lambda x: city_nhl(x))
    list_dict = []
    for group, frame in nhl_df.groupby('city'):
        # ratio = list(frame['W'].astype(int) / (frame['L'].astype(int) + frame['W'].astype(int)))
        win = np.sum(frame['W'].astype(int))
        all = np.sum(frame['L'].astype(int)) + np.sum(frame['W'].astype(int))
        ratio = win / all
        ratio_dict = {'City': group, 'Ratio': ratio}
        # print(ratio_dict)
        list_dict.append(ratio_dict)

    last_df = pd.DataFrame(list_dict).set_index('City')
    last_df = pd.merge(last_df, cities, how='inner', left_index=True, right_index=True)

    win_loss_by_region = list(last_df['Ratio'])
    population_by_region = list(last_df['Population (2016 est.)[8]'].astype(float))

    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    cor = stats.pearsonr(win_loss_by_region, population_by_region)
    return stats.pearsonr(population_by_region, win_loss_by_region)


print(nhl_correlation())