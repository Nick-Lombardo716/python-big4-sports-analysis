#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


# In[4]:


cities = pd.read_html("wikipedia_data.html")[1]
cities.drop(['Country', 'Pop.rank', 'B4', 'B6', 'MLS', 'CFL', 'NFL', 'MLB', 'NHL', 'NBA'], axis=1, inplace=True)
cities.rename(columns= {'Population (2016 est.)[8]': 'Population'}, inplace=True)
cities.rename(columns= {'Metropolitan area': 'city'}, inplace=True)


# In[23]:


mlb = pd.read_csv('mlb.csv')
mlb = mlb[mlb['year'] == 2018]
mlb = mlb[['team', 'W-L%']]

mlb['city'] = mlb['team'].apply(lambda x: x.rsplit(None, 1)[0])
mlb.loc[0,'city'] = 'Boston'
mlb.loc[1,'city'] = 'New York City'
mlb.loc[3,'city'] = 'Toronto'
mlb.loc[8,'city'] = 'Chicago'
mlb.loc[14,'city'] = 'Dallas–Fort Worth'
mlb.loc[18,'city'] = 'New York City'
mlb.loc[26,'city'] = 'Denver'
mlb.loc[27,'city'] = 'Phoenix'
mlb.loc[28,'city'] = 'San Francisco Bay Area'
mlb.loc[11,'city'] = 'San Francisco Bay Area'
mlb.loc[2,'city'] = 'Tampa Bay Area'
mlb.loc[6,'city'] = 'Minneapolis–Saint Paul'
mlb.loc[16,'city'] = 'Washington, D.C.'
mlb.loc[19,'city'] = 'Miami–Fort Lauderdale'

mlb['team'] = mlb['team'].apply(lambda x: x.rsplit(None, 1)[-1])
mlb.loc[0,'team'] = 'Red Sox'
mlb.loc[8,'team'] = 'White Sox'
mlb.loc[11,'team'] = 'Athletics'
mlb.loc[14,'team'] = 'Rangers'
mlb.loc[3,'team'] = 'Blue Jays'


# In[24]:


mlb.head(50)


# In[25]:


merged = pd.merge(mlb, cities, how='inner', on='city')
merged['Population'] = merged['Population'].astype(float)
merged['W-L%'] = merged['W-L%'].astype(float)
merged = merged[['city', 'team','W-L%', 'Population']]


# In[26]:


merged.head(50)


# In[27]:


final = merged.groupby('city').agg({'W-L%': 'mean', 'Population': 'mean'})


# In[28]:


final.head(50)


# In[29]:


population_by_region = final['Population']
win_loss_by_region = final['W-L%']

stats.pearsonr(population_by_region, win_loss_by_region)[0]


# In[ ]:





# In[ ]:




