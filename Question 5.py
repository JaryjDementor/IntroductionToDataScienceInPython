# Question 5
# In this question I would like you to explore the hypothesis that given that an area has two sports teams in different sports, those teams will perform the same within their respective sports. How I would like to see this explored is with a series of paired t-tests (so use ttest_rel) between all pairs of sports. Are there any sports where we can reject the null hypothesis? Again, average values where a sport has multiple teams in one region. Remember, you will only be including, for each sport, cities which have teams engaged in that sport, drop others as appropriate. This question is worth 20% of the grade for this assignment.

import pandas as pd
import numpy as np
import scipy.stats as stats
# import re


def team(team):
    return team.split()[-1]


def city(j, city):
    for i in city.index.values:
        if j in i:
            town = city.loc[i]
            return town[0]


mlb_df = pd.read_csv("mlb.csv")
nhl_df = pd.read_csv("nhl.csv")
nba_df = pd.read_csv("nba.csv")
nfl_df = pd.read_csv("nfl.csv")
cities = pd.read_html("wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
cities = cities.replace('\[\w+\d*\]', '', regex=True)


def MLB_cor():
    mlb_city = cities[['Metropolitan area', 'MLB']].replace('\[\w+\s\d*\]', '', regex=True).set_index('MLB')
    cities_m = cities[['Metropolitan area', 'Population (2016 est.)[8]', 'MLB']].replace('\[\w+\s\d*\]', '',regex=True).replace('—', '',regex=True).set_index('Metropolitan area')
    mlb_df_1 = mlb_df.where(mlb_df['year'] == 2018).dropna()
    mlb_df_1['city'] = mlb_df_1['team'].apply(lambda x: team(x))
    mlb_df_1['city'] = mlb_df_1['city'].apply(lambda x: city(x, mlb_city))
    mlb_df_1['city'].loc[0] = 'Boston'
    list_dict = []
    for group, frame in mlb_df_1.groupby('city'):
        win = np.sum(frame['W'].astype(int))
        all = np.sum(frame['L'].astype(int)) + np.sum(frame['W'].astype(int))
        ratio = win / all
        ratio_dict = {'City': group, 'Ratio': ratio}
        list_dict.append(ratio_dict)

    df = pd.DataFrame(list_dict).set_index('City')
    df = pd.merge(df, cities_m, how='inner', left_index=True, right_index=True).drop('Population (2016 est.)[8]', 1)
    #     print(df)
    return df


# MLB_c()

def NHL_cor():
    nhl_df_1 = nhl_df.where(nhl_df['year'] == 2018).dropna()
    nhl_df_1['team'] = nhl_df_1['team'].replace('\*', '', regex=True)
    nhl_city = cities[['Metropolitan area', 'NHL']].replace('\[\w+\s\d*\]', '', regex=True).set_index('NHL')
    cities_nh = cities[['Metropolitan area', 'Population (2016 est.)[8]', 'NHL']].replace('\[\w+\s\d*\]', '',regex=True).replace('—', '',regex=True).set_index('Metropolitan area')
    nhl_df_1['city'] = nhl_df_1['team'].apply(lambda x: team(x))
    nhl_df_1['city'] = nhl_df_1['city'].apply(lambda x: city(x, nhl_city))
    list_dict = []
    for group, frame in nhl_df_1.groupby('city'):
        win = np.sum(frame['W'].astype(int))
        all = np.sum(frame['L'].astype(int)) + np.sum(frame['W'].astype(int))
        ratio = win / all
        ratio_dict = {'City': group, 'Ratio': ratio}
        #         print(ratio_dict)
        list_dict.append(ratio_dict)

    df = pd.DataFrame(list_dict).set_index('City')
    df = pd.merge(df, cities_nh, how='inner', left_index=True, right_index=True).drop('Population (2016 est.)[8]', 1)
    return df


# NHL_cor()

def NBA_cor():
    nba_df_1 = nba_df.where(nba_df['year'] == 2018).dropna()
    nba_df_1['team'] = nba_df_1['team'].replace('\*', '', regex=True).replace('\(\d*\)', '', regex=True)
    nba_city = cities[['Metropolitan area', 'NBA']].replace('\[\w+\s\d*\]', '', regex=True).set_index('NBA')
    cities_nb = cities[['Metropolitan area', 'Population (2016 est.)[8]', 'NBA']].replace('\[\w+\s\d*\]', '',regex=True).replace('—', '',regex=True).set_index('Metropolitan area')
    nba_df_1['city'] = nba_df_1['team'].apply(lambda x: team(x))
    nba_df_1['city'] = nba_df_1['city'].apply(lambda x: city(x, nba_city))
    list_dict = []
    for group, frame in nba_df_1.groupby('city'):
        win = np.sum(frame['W'].astype(int))
        all = np.sum(frame['L'].astype(int)) + np.sum(frame['W'].astype(int))
        ratio = win / all
        ratio_dict = {'City': group, 'Ratio': ratio}
        list_dict.append(ratio_dict)

    df = pd.DataFrame(list_dict).set_index('City')
    df = pd.merge(df, cities_nb, how='inner', left_index=True, right_index=True).drop('Population (2016 est.)[8]', 1)
    return df


# NBA_cor()

def NFL_cor():
    nfl_city = cities[['Metropolitan area', 'NFL']].replace('\[\w+\s\d*\]', '', regex=True).set_index('NFL')
    cities_nf = cities[['Metropolitan area', 'Population (2016 est.)[8]', 'NFL']].replace('\[\w+\s\d*\]', '',regex=True).replace('—', '',regex=True).set_index('Metropolitan area')
    nfl_df_1 = nfl_df.where(nfl_df['year'] == 2018).replace('\*|\+', '', regex=True).dropna()
    nfl_df_1['city'] = nfl_df_1['team'].apply(lambda x: team(x))
    nfl_df_1['city'] = nfl_df_1['city'].apply(lambda x: city(x, nfl_city))
    list_dict = []
    for group, frame in nfl_df_1.groupby('city'):
        win = np.sum(frame['W'].astype(int))
        all = np.sum(frame['L'].astype(int)) + np.sum(frame['W'].astype(int))
        ratio = win / all
        ratio_dict = {'City': group, 'Ratio': ratio}
        list_dict.append(ratio_dict)
    df = pd.DataFrame(list_dict).set_index('City')
    df = pd.merge(df, cities_nf, how='inner', left_index=True, right_index=True).drop('Population (2016 est.)[8]', 1)
    return df


# NFL_cor()

MLB = MLB_cor()
NHL = NHL_cor()
NBA = NBA_cor()
NFL = NFL_cor()
MLB_NHL = pd.merge(MLB, NHL, left_index=True, right_index=True)
pval_MLB_NHL = stats.ttest_rel(MLB_NHL['Ratio_x'], MLB_NHL['Ratio_y'])
# pval_MLB_NHL[1]
MLB_NBA = pd.merge(MLB, NBA, left_index=True, right_index=True)
pval_MLB_NBA = stats.ttest_rel(MLB_NBA['Ratio_x'], MLB_NBA['Ratio_y'])
# pval_MLB_NBA[1]
# stats.ttest_rel
MLB_NFL = pd.merge(MLB, NFL, left_index=True, right_index=True)
pval_MLB_NFL = stats.ttest_rel(MLB_NFL['Ratio_x'], MLB_NFL['Ratio_y'])
# pval_MLB_NFL[1]
NHL_NBA = pd.merge(NHL, NBA, left_index=True, right_index=True)
pval_NHL_NBA = stats.ttest_rel(NHL_NBA['Ratio_x'], NHL_NBA['Ratio_y'])
# pval_NHL_NBA[1]
NHL_NFL = pd.merge(NHL, NFL, left_index=True, right_index=True)
pval_NHL_NFL = stats.ttest_rel(NHL_NFL['Ratio_x'], NHL_NFL['Ratio_y'])
# pval_NHL_NFL[1]
NBA_NFL = pd.merge(NBA, NFL, left_index=True, right_index=True)
pval_NBA_NFL = stats.ttest_rel(NBA_NFL['Ratio_x'], NBA_NFL['Ratio_y'])
print(pval_NHL_NBA[1])
