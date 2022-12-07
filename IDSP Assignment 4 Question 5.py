#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import re


# In[ ]:





# In[2]:


cities = pd.read_html("wikipedia_data.html")[1]
cities.drop(['Country', 'Pop.rank', 'B4', 'B6', 'MLS', 'CFL'], axis=1, inplace=True)
cities.rename(columns= {'Population (2016 est.)[8]': 'Population'}, inplace=True)
cities.rename(columns= {'Metropolitan area': 'city'}, inplace=True)
cities['NFL'] = cities['NFL'].str.replace(r"\[.*\]", "", regex=True)
cities['MLB'] = cities['MLB'].str.replace(r"\[.*\]", "", regex=True)
cities['NBA'] = cities['NBA'].str.replace(r"\[.*\]", "", regex=True)
cities['NHL'] = cities['NHL'].str.replace(r"\[.*\]", "", regex=True)


# In[3]:


cities.head(50)


# In[4]:


nfl = pd.read_csv('nfl.csv')
nfl = nfl[nfl['year'] == 2018]
nfl['team'] = nfl['team'].str.replace(r'\*', '', regex=True)
nfl['team'] = nfl['team'].str.replace(r'\+', '', regex=True)
nfl = nfl[~nfl.team.str.contains('AFC')]
nfl = nfl[~nfl.team.str.contains('NFC')]
nfl.reset_index(inplace=True)
nfl = nfl[['team', 'W-L%']]
nfl.rename(columns={'W-L%':'nfl_w/l'}, inplace=True)
nfl['nfl_w/l'] = nfl['nfl_w/l'].astype(float)

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

nfl_city = nfl.groupby('city').agg({'nfl_w/l':'mean'},inplace=True)


# In[5]:


mlb = pd.read_csv('mlb.csv')
mlb = mlb[mlb['year'] == 2018]
mlb = mlb[['team', 'W-L%']]
mlb.rename(columns={'W-L%':'mlb_w/l'}, inplace=True)
mlb['mlb_w/l'] = mlb['mlb_w/l'].astype(float)

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

mlb_city = mlb.groupby('city').agg({'mlb_w/l':'mean'},inplace=True)


# In[6]:


nba = pd.read_csv('nba.csv')
nba = nba[nba['year'] == 2018]
nba['team'] = nba['team'].str.replace(r'\*', '', regex=True)
nba['team'] = nba['team'].str.replace(r'\([0-9]+\)', '', regex=True)
nba = nba[['team', 'W/L%']]
nba.rename(columns={'W/L%':'nba_w/l'}, inplace=True)
nba['nba_w/l'] = nba['nba_w/l'].astype(float)

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

nba_city = nba.groupby('city').agg({'nba_w/l':'mean'},inplace=True)


# In[7]:


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

nhl['W'] = nhl['W'].astype(float)
nhl['L'] = nhl['L'].astype(float)
nhl['nhl_w/l'] = nhl['W'] / (nhl['W'] + nhl['L'])
nhl = nhl[['team', 'nhl_w/l', 'city']]

nhl_city = nhl.groupby('city').agg({'nhl_w/l':'mean'},inplace=True)


# In[8]:


merged = pd.merge(nfl_city, nba_city, how='outer', on='city')
merged = pd.merge(merged, nhl_city, how='outer', on='city')
merged = pd.merge(merged, mlb_city, how='outer', on='city')


# In[9]:


merged


# In[10]:


stats.ttest_rel(merged['nfl_w/l'], merged['nba_w/l'], nan_policy='omit')


# In[11]:


stats.ttest_rel(merged['nfl_w/l'], merged['nhl_w/l'], nan_policy='omit')


# In[12]:


stats.ttest_rel(merged['nfl_w/l'], merged['mlb_w/l'], nan_policy='omit')


# In[13]:


stats.ttest_rel(merged['nba_w/l'], merged['nhl_w/l'], nan_policy='omit')


# In[14]:


stats.ttest_rel(merged['nba_w/l'], merged['mlb_w/l'], nan_policy='omit')


# In[15]:


stats.ttest_rel(merged['mlb_w/l'], merged['nhl_w/l'], nan_policy='omit')


# In[ ]:




