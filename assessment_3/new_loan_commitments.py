import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import datetime as dt
import pydeck as pdk
import requests as req
import datetime
import time

st.title('New Loan Commitments')

# Load data
DATE_COLUMN = 'date'
DATA_URL = ('new_loan_commitments.csv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')


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

# region filter
region_input = st.sidebar.multiselect(
    'Region',
    data.groupby('region').count().reset_index()['region'].tolist())

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

st.write(subset)

# Line Chart

st.header('New Loan Commitments')
st.subheader(metric_name)

lineChart = alt.Chart(subset).mark_line().encode(
    x = alt.X('yearmonth(date):T', title='date'),
    y = metric,
    color = 'region',
).properties(
    width=800,
    height=600
)

st.altair_chart(lineChart)

# Map
st.header('Australia Map')
st.subheader('Map')
source = alt.topo_feature('https://raw.githubusercontent.com/simaQ/maps-data/master/Australia-states.geo.json', 'features')


baseMap = alt.Chart(source).mark_geoshape(
    fill='#666666',
    stroke='white'
).properties(
    width=800,
    height=600
).project('mercator')

#points = alt.Chart(subset).mark_circle().encode(
    #longitude='longitude:Q',
    #latitude='latitude:Q',
    #color=alt.Color('price:Q', title='Price of Airbnb'),
    #tooltip=['name:N','room_type:N','price:Q','neighbourhood:N']
#).properties(
    #title='Number of Airbnb Listings'
#)

st.altair_chart(baseMap)#+points)

data_url = 'https://raw.githubusercontent.com/simaQ/maps-data/master/Australia-states.geo.json'

states = req.get(data_url).json()

states['features'][0]['properties']['STATE_CODE'] = 20
states['features'][1]['properties']['STATE_CODE'] = 40
states['features'][2]['properties']['STATE_CODE'] = 60
states['features'][3]['properties']['STATE_CODE'] = 80
states['features'][4]['properties']['STATE_CODE'] = 100
states['features'][5]['properties']['STATE_CODE'] = 120
states['features'][6]['properties']['STATE_CODE'] = 140
states['features'][7]['properties']['STATE_CODE'] = 160
states['features'][8]['properties']['STATE_CODE'] = 180


# Set viewport for the deckgl map

initial_view = pdk.ViewState(
  latitude=-27.5,
  longitude=133,
  zoom=3,
  max_zoom=16,
  pitch=0,
  bearing=0
)

geojson = pdk.Layer(
    'GeoJsonLayer',
    states,
    opacity=0.5,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    pickable=True,
    get_fill_color='[0,0,properties.STATE_CODE]',
    get_line_color=[255, 255, 255]
)

r = pdk.Deck(
    layers=[geojson],
    initial_view_state=initial_view)

map = st.pydeck_chart(r)

animation = subset

if play:
    initial_view = pdk.ViewState(
        latitude=-27.5,
        longitude=133,
        zoom=3,
        max_zoom=16,
        pitch=0,
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
        get_fill_color='[255,properties.STATE_CODE,properties.STATE_CODE]',
        get_line_color=[255, 255, 255]
        )
    t = pdk.Deck(
        layers=[geojson],
        initial_view_state=initial_view,
        map_style="mapbox://styles/mapbox/light-v10",
        )
    
    # Render the deck.gl map in the Streamlit app as a Pydeck chart 
    date = subset['date'].unique()[0]
    timestamp = st.subheader(date)
    max_value = subset[metric].max()
    
    map = st.pydeck_chart(t)

    # Update the map for each month value
    for i in range(0, subset['date'].nunique()):
        
        new_date = subset['date'].unique()[i]
        
        timestamp.subheader(new_date)
        
        if len(region_input) > 0:
            selected_regions = region_input
        else:
            selected_regions = animation.groupby('region').count().reset_index()['region'].tolist()

        
        if 'New South Wales' in selected_regions:
            nsw = animation[animation['region'] == 'New South Wales'].iloc[i,3]
            states['features'][0]['properties']['STATE_CODE'] = 255 -((nsw/max_value) * 255)
        else:
            states['features'][0]['properties']['STATE_CODE'] = 255
            
        if 'Victoria' in selected_regions:
            vic = animation[animation['region'] == 'Victoria'].iloc[i,3]
            states['features'][1]['properties']['STATE_CODE'] = 255 -((vic/max_value) * 255)
        else:
            states['features'][1]['properties']['STATE_CODE'] = 255
            
        if 'Queensland' in selected_regions:
            qld = animation[animation['region'] == 'Queensland'].iloc[i,3]
            states['features'][2]['properties']['STATE_CODE'] = 255 -((qld/max_value) * 255)
        else:
            states['features'][2]['properties']['STATE_CODE'] = 255
            
        if 'South Australia' in selected_regions:
            sa = animation[animation['region'] == 'South Australia'].iloc[i,3]
            states['features'][3]['properties']['STATE_CODE'] = 255 -((sa/max_value) * 255)
        else:
            states['features'][3]['properties']['STATE_CODE'] = 255
            
        if 'Western Australia' in selected_regions:
            wa = animation[animation['region'] == 'Western Australia'].iloc[i,3]
            states['features'][4]['properties']['STATE_CODE'] = 255 -((wa/max_value) * 255)
        else:
            states['features'][4]['properties']['STATE_CODE'] = 255
            
        if 'Tasmania' in selected_regions:
            tas = animation[animation['region'] == 'Tasmania'].iloc[i,3]
            states['features'][5]['properties']['STATE_CODE'] = 255 -((tas/max_value) * 255)
        else:
            states['features'][5]['properties']['STATE_CODE'] = 255
            
        if 'Northern Territory' in selected_regions:
            nt = animation[animation['region'] == 'Northern Territory'].iloc[i,3]
            states['features'][6]['properties']['STATE_CODE'] = 255 -((nt/max_value) * 255)
        else:
            states['features'][6]['properties']['STATE_CODE'] = 255
            
        if 'Australian Capital Territory' in selected_regions:
            act = animation[animation['region'] == 'Australian Capital Territory'].iloc[i,3]
            states['features'][7]['properties']['STATE_CODE'] = 255 -((act/max_value) * 255)
        else:
            states['features'][7]['properties']['STATE_CODE'] = 255
            
        states['features'][8]['properties']['STATE_CODE'] = 255
       
        # Update the deck.gl map
        t.update()
    
        # Render the map
        map.pydeck_chart(t)
    
        # wait 0.3 second before go onto next day
        time.sleep(0.2)
else:
    st.write('Hit "Start Animation"')

