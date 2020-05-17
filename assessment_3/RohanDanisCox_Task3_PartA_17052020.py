# -*- coding: utf-8 -*-
"""
Created on Sun May 17 09:34:12 2020

@author: rohan
"""
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime as dt
import pydeck as pdk
import requests as req
import datetime
import time

st.title('First Home Buyers - New Loan Commitments')

# Load data
DATE_COLUMN = 'date'
DATA_URL = ('fhb_new_loan_commitments.csv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data


# Load data.
data = load_data()

# Sidebar widgets

# Filters UI

# Metric Filter
metric_name = st.sidebar.selectbox(
    'Metric', 
    ['Number of New Loan Commitments','Value of New Loan Commitments - In Millions'])
    
if 'Number of New Loan Commitments' in metric_name:
    metric = 'number'
else:
    metric = 'value'

# Date Filters
date_start = st.sidebar.date_input('Start Date', data['date'].min())
date_end = st.sidebar.date_input('End Date', data['date'].max())

# Series filter
series_input = st.sidebar.selectbox(
    'Series',
    data.groupby('series_type').count().reset_index()['series_type'].tolist())

# Region filter
region_input = st.sidebar.multiselect(
    'Region',
    data.groupby('region').count().reset_index()['region'].tolist())

# Animation play button
play = st.sidebar.button(
    label = 'Start Animation')
                                                
# Filter data
subset = data
# by metric
if len(metric_name) > 0:
    subset = data[['date','region','series_type',metric]]

# by series
if len(series_input) > 0:
    subset = subset[subset['series_type'] == series_input]
# by date
subset = subset[subset['date'] >= pd.to_datetime(date_start)]
subset = subset[subset['date'] <= pd.to_datetime(date_end)]

# by region
if len(region_input) > 0:
    subset = subset[subset['region'].isin(region_input)]

# Line Chart

st.header(metric_name)

lineChart = alt.Chart(subset).mark_line().encode(
    x = alt.X('yearmonth(date):T', title='date'),
    y = metric,
    color = 'region',
).properties(
    width=750,
    height=350
)

st.altair_chart(lineChart)

data_url = 'https://raw.githubusercontent.com/simaQ/maps-data/master/Australia-states.geo.json'

states = req.get(data_url).json()

### SET VALUES 
states['features'][0]['properties']['COLOUR'] = 255
states['features'][1]['properties']['COLOUR'] = 255
states['features'][2]['properties']['COLOUR'] = 255
states['features'][3]['properties']['COLOUR'] = 255
states['features'][4]['properties']['COLOUR'] = 255
states['features'][5]['properties']['COLOUR'] = 255
states['features'][6]['properties']['COLOUR'] = 255
states['features'][7]['properties']['COLOUR'] = 255
states['features'][8]['properties']['COLOUR'] = 255

states['features'][0]['properties']['HEIGHT'] = 0
states['features'][1]['properties']['HEIGHT'] = 0
states['features'][2]['properties']['HEIGHT'] = 0
states['features'][3]['properties']['HEIGHT'] = 0
states['features'][4]['properties']['HEIGHT'] = 0
states['features'][5]['properties']['HEIGHT'] = 0
states['features'][6]['properties']['HEIGHT'] = 0
states['features'][7]['properties']['HEIGHT'] = 0
states['features'][8]['properties']['HEIGHT'] = 0

animation = subset

if play:
    initial_view = pdk.ViewState(
        latitude=-27.5,
        longitude=133,
        zoom=3,
        max_zoom=16,
        pitch=45,
        bearing=0
        )
    geojson = pdk.Layer(
        'GeoJsonLayer',
        states,
        opacity=0.9,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        pickable=True,
        get_elevation ='properties.HEIGHT*150',
        get_fill_color='[255,properties.COLOUR,properties.COLOUR]',
        get_line_color=[255, 255, 255]
        )
    t = pdk.Deck(
        layers=[geojson],
        initial_view_state=initial_view,
        map_style="mapbox://styles/mapbox/light-v10",
        #height = 350
        )

    
    # Render the deck.gl map in the Streamlit app as a Pydeck chart 
    date = subset['date'].unique()[0]
    month = month = np.datetime64(date, 'M')
    timestamp = st.subheader(month)
    
    max_value = subset[metric].max()
    
    map = st.pydeck_chart(t)

    # Update the map for each month value
    for i in range(0, subset['date'].nunique()):
        
        new_date = subset['date'].unique()[i]
        new_month = np.datetime64(new_date, 'M')
        
        timestamp.subheader(new_month)
        
        if len(region_input) > 0:
            selected_regions = region_input
        else:
            selected_regions = animation.groupby('region').count().reset_index()['region'].tolist()

        
        if 'New South Wales' in selected_regions:
            nsw = int(animation[animation['region'] == 'New South Wales'].iloc[i,3])
            states['features'][0]['properties']['COLOUR'] = 255 -((nsw/max_value) * 255)
            states['features'][0]['properties']['HEIGHT'] = nsw
            
        if 'Victoria' in selected_regions:
            vic = int(animation[animation['region'] == 'Victoria'].iloc[i,3])
            states['features'][1]['properties']['COLOUR'] = 255 -((vic/max_value) * 255)
            states['features'][1]['properties']['HEIGHT'] = vic
            
        if 'Queensland' in selected_regions:
            qld = int(animation[animation['region'] == 'Queensland'].iloc[i,3])
            states['features'][2]['properties']['COLOUR'] = 255 -((qld/max_value) * 255)
            states['features'][2]['properties']['HEIGHT'] = qld
            
        if 'South Australia' in selected_regions:
            sa = int(animation[animation['region'] == 'South Australia'].iloc[i,3])
            states['features'][3]['properties']['COLOUR'] = 255 -((sa/max_value) * 255)
            states['features'][3]['properties']['HEIGHT'] = sa
            
        if 'Western Australia' in selected_regions:
            wa = int(animation[animation['region'] == 'Western Australia'].iloc[i,3])
            states['features'][4]['properties']['COLOUR'] = 255 -((wa/max_value) * 255)
            states['features'][4]['properties']['HEIGHT'] = wa
            
        if 'Tasmania' in selected_regions:
            tas = int(animation[animation['region'] == 'Tasmania'].iloc[i,3])
            states['features'][5]['properties']['COLOUR'] = 255 -((tas/max_value) * 255)
            states['features'][5]['properties']['HEIGHT'] = tas
            
        if 'Northern Territory' in selected_regions:
            nt = int(animation[animation['region'] == 'Northern Territory'].iloc[i,3])
            states['features'][6]['properties']['COLOUR'] = 255 -((nt/max_value) * 255)
            states['features'][6]['properties']['HEIGHT'] = nt
            
        if 'Australian Capital Territory' in selected_regions:
            act = int(animation[animation['region'] == 'Australian Capital Territory'].iloc[i,3])
            states['features'][7]['properties']['COLOUR'] = 255 -((act/max_value) * 255)
            states['features'][7]['properties']['HEIGHT'] = act
        
        # Update the deck.gl map
        t.update()
    
        # Render the map
        map.pydeck_chart(t)
    
        # wait 0.3 second before go onto next day
        time.sleep(0.2)
else:
    st.write('Hit "Start Animation"')