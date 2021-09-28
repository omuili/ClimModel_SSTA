#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cdsapi

c = cdsapi.Client()

c.retrieve(
    'seasonal-postprocessed-single-levels',
    {
        'format': 'grib',
        'originating_centre': 'ecmwf',
        'system': '5',
        'variable': 'sea_surface_temperature_anomaly',
        'product_type': 'ensemble_mean',
        'year': '2018',
        'month': '12',
        'leadtime_month': '3',
    },
    'download.grib')


# In[2]:


pip install plotly --upgrade


# In[3]:


pip install xarray


# In[4]:


pip install dash


# In[5]:


pip install plotly==5.3.1


# In[6]:


pip install chart_studio


# In[7]:


import pandas as pd


# In[8]:


import xarray as xr
import chart_studio.plotly as py
import plotly.offline as py_off
import plotly.graph_objects as go
import numpy as np
from scipy.io import netcdf


# In[9]:


from plotly.graph_objs import Scattermapbox


# In[10]:


from plotly.graph_objs.scattermapbox import Marker


# In[48]:


from plotly.graph_objs import Layout


# In[58]:


import plotly


# In[13]:


import chart_studio


# In[64]:


from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()


# In[14]:


chart_studio.tools.set_credentials_file(username='olanrewaju.muili@gmail.com', api_key='103800:0d682f78-6a06-4c0a-ab68-f6d1c72a254d')


# In[15]:


mapbox_access_token = 'pk.eyJ1Ijoib2xhbnJld2FqdW11aWxpIiwiYSI6ImNrdTM0dTA1NTJubXEydXFtMHJxdWNzeHMifQ.aApqHZKCbOAM9UcNVD7QXw'


# In[16]:


conda install netcdf4


# In[17]:


from netCDF4 import Dataset


# In[18]:


import cdsapi

c = cdsapi.Client()

c.retrieve(
    'seasonal-postprocessed-single-levels',
    {
        'originating_centre':'ecmwf',
        'system':'5',
        'variable':'sea_surface_temperature_anomaly',
        'product_type':'ensemble_mean',
        'year':'2019',
        'month':'01',
        'leadtime_month':'3',
        'format':'netcdf'
    },
    'sst.nc')


# In[19]:


f_path = 'C:\\Users\\MUILI OLANREWAJU\\sst.nc'


# In[20]:


f = Dataset(f_path)


# In[21]:


f


# In[22]:


f.variables.keys()


# In[23]:


ds2 = xr.open_dataset(xr.backends.NetCDF4DataStore(f))


# In[24]:


df2 = ds2.to_dataframe()


# In[25]:


df2.index[0]


# In[26]:


df_sub = df2.iloc[df2.index.get_level_values('time') == '2019-03-01']


# In[27]:


df_sub.tail()


# In[28]:


len(df_sub.index.get_level_values('longitude')), len(df_sub['ssta']) 


# In[29]:


step = 1.0


# In[30]:


to_bin = lambda x: np.floor(x / step) * step


# In[31]:


df_sub["latbin"] = df_sub.index.get_level_values('latitude').map(to_bin)


# In[32]:


df_sub["lonbin"] = df_sub.index.get_level_values('longitude').map(to_bin)


# In[33]:


groups = df_sub.groupby(['latbin', 'lonbin'])


# In[34]:


df_flat = df_sub.drop_duplicates(subset=['latbin', 'lonbin'])


# In[35]:


df_flat.head()


# In[36]:


len(df_flat['lonbin'])


# In[37]:


df_no_nan = df_flat[np.isfinite(df_flat['ssta'])]


# In[38]:


len(df_no_nan)


# In[39]:


df_no_nan.tail()


# In[40]:


#snow = df_no_nan['sfara'].values*2419200*39*10


# In[41]:


df_no_nan = df_no_nan[(df_no_nan.latbin < 90.0) & (df_no_nan.latbin > -90.0)]


# In[42]:


colorscale= [[0.0, '#171c42'], [0.07692307692307693, '#263583'], [0.15384615384615385, '#1a58af'], [0.23076923076923078, '#1a7ebd'], [0.3076923076923077, '#619fbc'], [0.38461538461538464, '#9ebdc8'], [0.46153846153846156, '#d2d8dc'], [0.5384615384615384, '#e6d2cf'], [0.6153846153846154, '#daa998'], [0.6923076923076923, '#cc7b60'], [0.7692307692307693, '#b94d36'], [0.8461538461538461, '#9d2127'], [0.9230769230769231, '#6e0e24'], [1.0, '#3c0911']]


# In[43]:


#colorscale = [[0, 'rgb(54, 50, 153)'], [0.35, 'rgb(17, 123, 215)'],
#                [0.5, 'rgb(37, 180, 167)'], [0.6, 'rgb(134, 191, 118)'],
#                [0.7, 'rgb(249, 210, 41)'], [1.0, 'rgb(244, 236, 21)']]


# In[44]:


import plotly.express as px


# In[45]:


data = []
data.append(
    Scattermapbox(
        lon=df_no_nan['lonbin'].values,
        lat=df_no_nan['latbin'].values,
        mode='markers',
        text=df_no_nan['ssta'].values,
        marker=Marker(
            cmax=2.5,
            cmin=-2.5,
            color=df_no_nan['ssta'].values,
            colorscale=colorscale
        ),
    )
)


# In[49]:


layout = Layout(
    margin=dict(t=0,b=0,r=0,l=0),
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=38,
            lon=-94
        ),
        pitch=0,
        zoom=0,
        style='dark'
    ),
)


# In[65]:


fig = dict(data=data, layout=layout)
plotly.offline.iplot(fig, filename='ecmwf_sst.html')


# In[ ]:




