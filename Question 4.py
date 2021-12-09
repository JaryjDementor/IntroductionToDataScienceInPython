# Question 4
# For this question, calculate the win/loss ratio's correlation with the population of the city it is in for the NFL using 2018 data.

import pandas as pd
import numpy as np
import scipy.stats as stats

def team_nfl(team):
    return team.split()[-1]

def city_nfl(j):
    for i in nfl_city.index.values:
        if j in i:
            town=nfl_city.loc[i]
            return town[0]
nfl_df = pd.read_csv("nfl.csv")
cities = pd.read_html("wikipedia_data.html")[1]
cities = cities.iloc[:-1, [0, 3, 5, 6, 7, 8]]
nfl_city=cities[['Metropolitan area','NFL']].replace('\[\w+\s\d*\]','',regex=True).set_index('NFL')
cities=cities[['Metropolitan area','Population (2016 est.)[8]']].replace('\[\w+\s\d*\]','',regex=True).replace('—','',regex=True).set_index('Metropolitan area')
nfl_df=nfl_df.where(nfl_df['year']==2018).replace('\*|\+','',regex=True).dropna()
def nfl_correlation():
   # YOUR CODE HERE
    # raise NotImplementedError()
    nfl_df['city']=nfl_df['team'].apply(lambda x: team_nfl(x))
    nfl_df['city']=nfl_df['city'].apply(lambda x: city_nfl(x))
    list_dict=[]
    for group,frame in nfl_df.groupby('city'):
        win=np.sum(frame['W'].astype(int))
        all=np.sum(frame['L'].astype(int))+np.sum(frame['W'].astype(int))
        ratio=win/all
        ratio_dict={'City':group,'Ratio':ratio}
        list_dict.append(ratio_dict)
    last_df=pd.DataFrame(list_dict).set_index('City')
    last_df=pd.merge(last_df,cities, how='inner',left_index=True,right_index=True)
    win_loss_by_region=list(last_df['Ratio'])
    population_by_region=list(last_df['Population (2016 est.)[8]'].astype(float))
#     print(len(population_by_region)
    return stats.pearsonr(population_by_region, win_loss_by_region)
print(nfl_correlation())
