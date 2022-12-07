#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


# In[29]:


cities = pd.read_html("wikipedia_data.html")[1]
cities.drop(['Country', 'Pop.rank', 'B4', 'B6', 'MLS', 'CFL', 'NFL', 'MLB', 'NHL', 'NBA'], axis=1, inplace=True)
cities.rename(columns= {'Population (2016 est.)[8]': 'Population'}, inplace=True)
cities.rename(columns= {'Metropolitan area': 'city'}, inplace=True)


# In[22]:


nfl = pd.read_csv('nfl.csv')
nfl = nfl[nfl['year'] == 2018]
nfl['team'] = nfl['team'].str.replace(r'\*', '', regex=True)
nfl['team'] = nfl['team'].str.replace(r'\+', '', regex=True)
nfl = nfl[~nfl.team.str.contains('AFC')]
nfl = nfl[~nfl.team.str.contains('NFC')]
nfl.reset_index(inplace=True)
nfl = nfl[['team', 'W-L%']]

nfl['city'] = nfl['team'].apply(lambda x: x.rsplit(None, 1)[0])
nfl.loc[3,'city'] = 'New York City'
nfl.loc[15,'city'] = 'San Francisco Bay Area'
nfl.loc[19,'city'] = 'New York City'
nfl.loc[21,'city'] = 'Minneapolis–Saint Paul'
nfl.loc[25,'city'] = 'Charlotte'
nfl.loc[30,'city'] = 'San Francisco Bay Area'
nfl.loc[0,'city'] = 'Boston'
nfl.loc[1,'city'] = 'Miami–Fort Lauderdale'
nfl.loc[10,'city'] = 'Nashville'
nfl.loc[16,'city'] = 'Dallas–Fort Worth'
nfl.loc[18,'city'] = 'Washington, D.C.'
nfl.loc[27,'city'] = 'Tampa Bay Area'
nfl.loc[31,'city'] = 'Phoenix'

nfl['team'] = nfl['team'].apply(lambda x: x.rsplit(None, 1)[-1])


# In[23]:


nfl.head(50)


# In[24]:


merged = pd.merge(nfl, cities, how='inner', on='city')
merged['W-L%'] = merged['W-L%'].astype(float)
merged['Population'] =merged['Population'].astype(float)
merged = merged[['city', 'team', 'W-L%', 'Population']]


# In[25]:


merged.head(50)


# In[26]:


final = merged.groupby('city').agg({'W-L%':'mean', 'Population':'mean'}, inplace=True)


# In[27]:


final.head(50)


# In[28]:


population_by_region = final['Population']
win_loss_by_region = final['W-L%']

stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[ ]:





# In[ ]:




