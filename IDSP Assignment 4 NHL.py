#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


# In[3]:


nl = pd.read_csv('nhl.csv')
nl.head()


# In[8]:


nhl = pd.read_csv('nhl.csv')
nhl = nhl[nhl['year'] == 2018]
nhl['team'] = nhl['team'].str.replace(r'\*', '', regex=True)
nhl = nhl[['team', 'W', 'L']]
nhl = nhl[~nhl.team.str.contains('Division')]
nhl['city'] = nhl['team'].map({
    'Tampa Bay Lightning':'Tampa Bay Area',
     'Boston Bruins':'Boston',
     'Toronto Maple Leafs':'Toronto',
     'Florida Panthers':'Miami–Fort Lauderdale',
     'Detroit Red Wings':'Detroit',
     'Montreal Canadiens':'Montreal',
     'Ottawa Senators':'Ottawa',
     'Buffalo Sabres':'Buffalo',
     'Washington Capitals':'Washington, D.C.',
     'Pittsburgh Penguins':'Pittsburgh',
     'Philadelphia Flyers':'Philadelphia',
     'Columbus Blue Jackets':'Columbus',
     'New Jersey Devils':'New York City',
     'Carolina Hurricanes':'Raleigh',
     'New York Islanders':'New York City',
     'New York Rangers':'New York City',
     'Nashville Predators':'Nashville',
     'Winnipeg Jets':'Winnipeg',
     'Minnesota Wild':'Minneapolis–Saint Paul',
     'Colorado Avalanche':'Denver',
     'St. Louis Blues':'St. Louis',
     'Dallas Stars':'Dallas–Fort Worth',
     'Chicago Blackhawks':'Chicago',
     'Vegas Golden Knights':'Las Vegas',
     'Anaheim Ducks':'Los Angeles',
     'San Jose Sharks':'San Francisco Bay Area',
     'Los Angeles Kings':'Los Angeles',
     'Calgary Flames':'Calgary',
     'Edmonton Oilers':'Edmonton',
     'Vancouver Canucks':'Vancouver',
     'Arizona Coyotes':'Phoenix'})

nhl['team'] = nhl['team'].apply(lambda x: x.rsplit(None, 1)[-1])
nhl.loc[5, 'team'] = 'Red Wings'
nhl.loc[3, 'team'] = 'Maple Leafs'
nhl.loc[13, 'team'] = 'Blue Jackets'
nhl.loc[27, 'team'] = 'Golden Knights'


# In[9]:


nhl


# In[7]:


cities = pd.read_html("wikipedia_data.html")[1]
cities.drop(['Country', 'Pop.rank', 'B4', 'B6', 'MLS', 'CFL'], axis=1, inplace=True)
cities.rename(columns= {'Population (2016 est.)[8]': 'Population'}, inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "", regex=True)
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "", regex=True)
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "", regex=True)
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "", regex=True)
cities.rename(columns= {'Metropolitan area': 'city'}, inplace=True)


# In[41]:


cities.head(50)


# In[8]:


merged = pd.merge(nhl, cities, how='inner', on='city' )
merged.drop(['NFL', 'MLB', 'NBA', 'NHL'], axis=1, inplace=True)
merged['W'] = merged['W'].astype(float)
merged['L'] = merged['L'].astype(float)
merged['Population'] = merged['Population'].astype(float)


merged['W/L Ratio'] = merged['W'] / (merged['W'] + merged['L'])


# In[9]:


merged = merged[['city', 'team', 'Population', 'W', 'L', 'W/L Ratio']]


# In[10]:


merged.shape


# In[11]:


merged.head(50)


# In[12]:


final = merged.groupby('city').agg({'W/L Ratio': 'mean', 'Population': 'mean'})


# In[13]:


final.shape


# In[46]:


final.head(32)


# In[14]:


final.shape


# In[15]:


population_by_region = final['Population']
win_loss_by_region = final['W/L Ratio']


# In[16]:


len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"


# In[17]:


len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"


# In[25]:


#first number is statistic, second number is pvalue
stats.pearsonr(population_by_region, win_loss_by_region)


# In[27]:


np.float64(stats.pearsonr(win_loss_by_region, population_by_region)[0])


# In[23]:


stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[ ]:




