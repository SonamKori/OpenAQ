#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip install py-openaq
import pandas as pd
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import openaq
import warnings
warnings.simplefilter('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


# Set major seaborn asthetics
sns.set("notebook", style='ticks', font_scale=1.0)

# Increase the quality of inline plots
mpl.rcParams['figure.dpi']= 500


# In[3]:


# initiate an instance of the openaq.OpenAQ
api = openaq.OpenAQ()


# In[4]:


resp = api.cities(df=True, limit=10000)

# display the first 10 rows
resp.info()


# In[5]:


#  India
print (resp.query("country == 'IN'"))


# In[6]:


# access the json-formatted data
status, resp = api.fetches(limit=1)

# Print out the meta info
resp['meta']


# In[7]:


#  listing off all the parameters available
res = api.parameters(df=True)

print (res)


# In[8]:


#  list of measurement locations 
res = api.locations(df=True)

res.info()


# In[9]:


res = api.locations(city='Delhi', df=True)
res.iloc[0]


# In[10]:


res = api.locations(city='Delhi', parameter='pm25', df=True)

res.iloc[0]


# In[11]:


res = api.latest(city='Delhi', parameter='o3' , df=True)

res.head()


# In[12]:


re = api.parameters(country = 'IN',df=True)
re.head()


# In[13]:


res = api.measurements(city='Delhi', parameter='pm25', limit=10000, df=True)

# Print out the statistics on a per-location basiss
res.groupby(['location'])['value'].describe()


# In[14]:


fig, ax = plt.subplots(1, figsize=(10, 6))

for group, df in res.groupby('location'):
    # Query the data to only get positive values and resample to hourly
    _df = df.query("value >= 0.0").resample('1h').mean()

    _df.value.plot(ax=ax, label=group)

ax.legend(loc='best')
ax.set_ylabel("$PM_{2.5}$  [$\mu g m^{-3}$]", fontsize=20)
ax.set_xlabel("")
sns.despine(offset=5)

plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

plt.show()


# In[15]:


fig, ax = plt.subplots(1, figsize=(14,7))

ax = sns.boxplot(
    x='location',
    y='value',
    data=res.query("value >= 0.0"),
    fliersize=0,
    palette='deep',
    ax=ax)

ax.set_ylim([0, 750])
ax.set_ylabel("$PM_{2.5}\;[\mu gm^{-3}]$", fontsize=18)
ax.set_xlabel("")

sns.despine(offset=10)

plt.xticks(rotation=90)
plt.show()


# In[16]:


res = api.measurements(city='Delhi', parameter='so2', limit=10000, df=True)

# Print out the statistics on a per-location basiss
res.groupby(['location'])['value'].describe()


# In[17]:


fig, ax = plt.subplots(1, figsize=(10, 5))

for group, df in res.groupby('location'):
    # Query the data to only get positive values and resample to hourly
    _df = df.query("value >= 0.0").resample('6h').mean()

    # Convert from ppm to ppb
    _df['value'] *= 1e3

    # Multiply the value by 1000 to get from ppm to ppb
    _df.value.plot(ax=ax, label=group)

#ax.legend(loc='best')
ax.set_ylabel("$SO_2 \; [ppb]$", fontsize=18)
ax.set_xlabel("")

sns.despine(offset=5)

plt.show()


# In[ ]:




