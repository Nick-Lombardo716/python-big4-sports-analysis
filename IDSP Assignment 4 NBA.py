#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


# In[76]:


cities = pd.read_html("wikipedia_data.html")[1]
cities.drop(['Country', 'Pop.rank', 'B4', 'B6', 'MLS', 'CFL', 'NFL', 'MLB', 'NHL', 'NBA'], axis=1, inplace=True)
cities.rename(columns= {'Population (2016 est.)[8]': 'Population'}, inplace=True)
cities.rename(columns= {'Metropolitan area': 'city'}, inplace=True)


# In[70]:


nba = pd.read_csv('nba.csv')
nba = nba[nba['year'] == 2018]
nba['team'] = nba['team'].str.replace(r'\*', '', regex=True)
nba['team'] = nba['team'].str.replace(r'\([0-9]+\)', '', regex=True)
nba = nba[['team', 'W/L%']]

nba['city'] = nba['team'].apply(lambda x: x.rsplit(None, 1)[0])
nba.loc[4,'city'] = 'Indianapolis'
nba.loc[7,'city'] = 'Washington, D.C.'
nba.loc[11,'city'] = 'New York City'
nba.loc[16,'city'] = 'San Francisco Bay Area'
nba.loc[19,'city'] = 'Salt Lake City'
nba.loc[22,'city'] = 'Minneapolis–Saint Paul'
nba.loc[27,'city'] = 'Dallas–Fort Worth'
nba.loc[17,'city'] = 'Portland'

nba['team'] = nba['team'].apply(lambda x: x.rsplit(None, 1)[-1])
nba.loc[4,'team'] = 'Pacers'
nba.loc[7,'team'] = 'Wizards'
nba.loc[11,'team'] = 'Thunder'
nba.loc[16,'team'] = 'Golden State Warriors'


# In[83]:


merged = pd.merge(nba, cities, how='inner', on='city')
merged['W/L%'] = merged['W/L%'].astype(float)
merged['Population'] =merged['Population'].astype(float)
merged = merged[['city', 'team', 'W/L%', 'Population']]


# In[87]:


final = merged.groupby('city').agg({'W/L%':'mean', 'Population':'mean'}, inplace=True)


# In[91]:


population_by_region = final['Population']
win_loss_by_region = final['W/L%']

stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[50]:


dict_map = {
    'Toronto Raptors':'Toronto',
    'Boston Celtics':'Boston',
    'Philadelphia 76ers':'Philadelphia',
    'Cleveland Cavaliers':'Cleveland',
    'Indiana Pacers':'Indianapolis',
    'Miami Heat':'Miami',
    'Milwaukee Bucks':'Milwaukee',
    'Washington Wizards':'Washington, D.C.',
    'Detroit Pistons':'Detroit',
    'Charlotte Hornets':'Charlotte',
    'New York Knicks':'New York City',
    'Brooklyn Nets':'New York City',
    'Chicago Bulls':'Chicago',
    'Orlando Magic':'Orlando',
    'Atlanta Hawks':'Atlanta',
    'Houston Rockets':'Houston',
    'Golden State Warriors':'San Francisco Bay Area',
    'Portland Trail Blazers':'Portland',
    'Oklahoma City Thunder':'Oklahoma City',
    'Utah Jazz':'Salt Lake City',
    'New Orleans Pelicans':'New Orleans',
    'San Antonio Spurs':'San Antonio',
    'Minnesota Timberwolves':'Minneapolis–Saint Paul',
    'Denver Nuggets':'Denver',
    'Los Angeles Clippers':'Los Angeles',
    'Los Angeles Lakers':'Los Angeles',
    'Sacramento Kings':'Sacramento',
    'Dallas Mavericks':'Dallas',
    'Memphis Grizzlies':'Memphis',
    'Phoenix Suns':'Phoenix'}
nba['city'] = nba['team'].map(dict_map)


# In[ ]:



'''nba['city'] = nba['team'].map({
    'Toronto Raptors':'Toronto',
    'Boston Celtics':'Boston',
    'Philadelphia 76ers':'Philadelphia',
    'Cleveland Cavaliers':'Cleveland',
    'Indiana Pacers':'Indianapolis',
    'Miami Heat':'Miami',
    'Milwaukee Bucks':'Milwaukee',
    'Washington Wizards':'Washington, D.C.',
    'Detroit Pistons':'Detroit',
    'Charlotte Hornets':'Charlotte',
    'New York Knicks':'New York City',
    'Brooklyn Nets':'New York City',
    'Chicago Bulls':'Chicago',
    'Orlando Magic':'Orlando',
    'Atlanta Hawks':'Atlanta',
    'Houston Rockets':'Houston',
    'Golden State Warriors':'San Francisco Bay Area',
    'Portland Trail Blazers':'Portland',
    'Oklahoma City Thunder':'Oklahoma City',
    'Utah Jazz':'Salt Lake City',
    'New Orleans Pelicans':'New Orleans',
    'San Antonio Spurs':'San Antonio',
    'Minnesota Timberwolves':'Minneapolis–Saint Paul',
    'Denver Nuggets':'Denver',
    'Los Angeles Clippers':'Los Angeles',
    'Los Angeles Lakers':'Los Angeles',
    'Sacramento Kings':'Sacramento',
    'Dallas Mavericks':'Dallas',
    'Memphis Grizzlies':'Memphis',
    'Phoenix Suns':'Phoenix'})'''


# In[92]:


nba.head()


# In[93]:


merged.head()


# In[94]:


final.head()


# In[ ]:




