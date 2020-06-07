# -*- coding: utf-8 -*-
"""
Created on Sun May 17 09:34:12 2020
@author: rohan
"""
import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import pydeck as pdk
import requests as req
import datetime
import time
import plotly.express as px
import plotly.subplots as sp

### Load data

DATE_COLUMN = 'date'
DATA_URL = ('fhb_new_loan_commitments.csv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data = load_data()

### Set up sections

# App Sections
section = st.sidebar.selectbox(
    'Section',
    ['Introduction','Line Plot','Bubble Chart','Map Animation'])

### Build intro
if section == 'Introduction':
    st.title('First Home Buyers - New Loan Commitments')
    st.write('')
    st.write('This streamlit application is available to users to explore the impact of first home buyer incentives in Australia. Most of the visualisations work better on wide-screen mode, which can be selected from the settings section of the options in the top right. Use the section selector in the sidebar to move between plots.')
    st.write('For each section you will need to make selections from the sidebar on the left. These options will then be visualised given the respective section selected. The line plot is dynamic and can be adjusted by using the drag date filter or selecting parts of the chart. Similarly, the bubble chart includes a slider and animation button for navigating date. The map animation allows the user to select the start and end date for the animation using the slider.')

### Build Line Plot/Map animation
if section in ["Line Plot", "Map Animation"]:
    
    # New Loan Commitment Filter
    
    if section in "Line Plot":
        metric_name = st.sidebar.selectbox(
            'New Loan Commitments for First Home Buyers', 
            ['Loans',
             'Value ($)',
             'Loans per 100,000 people',
             'Value per person ($)'])
   
    elif section in "Map Animation":
        metric_name = st.sidebar.selectbox(
            'New Loan Commitments for First Home Buyers - Mapped to Colour',
            ['Loans',
             'Value ($)',
             'Loans per 100,000 people',
             'Value per person ($)'])
        
    if 'Loans per 100,000 people' in metric_name:
        metric = 'new_loan_commitments_per_100000'
    elif 'Loans' in metric_name:
        metric = 'total_new_loan_commitments'
    elif 'Value ($)' in metric_name:
        metric = 'value_in_millions'
    elif 'Value per person ($)' in metric_name:
        metric = 'value_per_person'
        
    # Incentive Filter
    if section in "Line Plot": 
        incentive_name = st.sidebar.selectbox(
            'Maximum Benefit Available for First Home Owners', 
            ['Dollar Value',
             'As % of Median House Price'])
    elif section in "Map Animation": 
        incentive_name = st.sidebar.selectbox(
            'Maximum Benefit Available for First Home Owners - Mapped to Elevation', 
            ['Dollar Value',
             'As % of Median House Price'])
    
    # Type of Incentive Filter
    incentive_type = st.sidebar.selectbox(
        'Type of Incentive',
        ['All','First Home Owner Grant','First Home Owner Boost','Duty Concession','Other'])
    
    option = incentive_type
    
    
    if 'As % of Median House Price' in incentive_name:
        incentive = 'max_benefit_as_percent_median_house_price'
    elif 'Dollar Value' in incentive_name:
        incentive = 'max_benefit_available'
    
    # Region filter
    region_input = st.sidebar.multiselect(
        'Region',
        data.groupby('region').count().reset_index()['region'].tolist())
    
    # Series filter
    series_input = st.sidebar.selectbox(
        'Series',
        ['Trend','Seasonally Adjusted','Original'])
    
    ### Line Plot Section
                                    
    # Filter data
    subset = data
    subsetter = [metric,incentive]
    
    # by metric
    subset = subset[subset['name'].isin(subsetter)]
    
    # by type 
    subset = subset[subset['type'] == option]
    
    # by series
    if len(series_input) > 0:
        subset = subset[subset['series_type'] == series_input]
    
    # by region
    if len(region_input) > 0:
        subset = subset[subset['region'].isin(region_input)]
    
    # Create plotly line chart    
    plotly_line = px.line(subset, x='date', 
                          y= 'value',
                          color='region',
                          facet_row = 'facet',
                          width = 900,
                          height = 700,
                          hover_data = ['schemes'],
                          title = "Comparing First Home Buyer Loan Commitments to Maximum Available Incentives")
    
    
    # Create x-axis slider and y axis names
    plotly_line.update_layout(xaxis_rangeslider_visible=True,
                              xaxis_rangeslider_thickness=0.1,
                              xaxis_title = "Date",
                              yaxis_title = incentive_name,
                              yaxis2_title = metric_name,
                              legend_title_text='State or Territory')
    
    # Fix annotations for facets
    for a in plotly_line.layout.annotations:
        a.text = a.text.split("=")[1]
        a.textangle = 0
        a.x = a.x - 0.95
        a.y = a.y + 0.2
        
    # Fix tick labels for % metric
    if 'As % of Median House Price' in incentive_name:
        plotly_line.update_layout(yaxis_tickformat = '%')
    
    # Build section
    if section == 'Line Plot':
        st.plotly_chart(plotly_line)
    
    ### Map Section
    
    # Obtain geojson
    data_url = 'https://raw.githubusercontent.com/simaQ/maps-data/master/Australia-states.geo.json'
    states = req.get(data_url).json()
    
    # Set values for shape features
    for i in range(0,9):
        states['features'][i]['properties']['COLOUR'] = 255
        states['features'][i]['properties']['HEIGHT'] = 0
    
    # Build the map
    
    if section == 'Map Animation':
        value = st.slider('Choose the start and end month for the animation', 
                                           min_value = 0, 
                                           max_value = 211,
                                           value = [0,
                                                    211])
        #value = st.slider("Select the starting month", 0, 212, 0, 1)
        selected_date_raw = subset['date'].unique()
        starting_date = selected_date_raw[value[0]]
        ending_date = selected_date_raw[value[1]]
        start_month = np.datetime64(starting_date, 'M')
        end_month = np.datetime64(ending_date, 'M')
        st.write(start_month,' to ', end_month)
        play = st.button(
            label = 'Animate map')
                
    if section == 'Map Animation':
        if play:
            initial_view = pdk.ViewState(
                latitude=-29.5,
                longitude=133,
                zoom=3,
                max_zoom=16,
                pitch=45,
                bearing=0,
                height = 450
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
                get_elevation ='properties.HEIGHT',
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
            chosen_subset = subset[subset['date'] >= starting_date]
            chosen_subset = chosen_subset[chosen_subset['date'] <= ending_date]
            date = chosen_subset['date'].unique()[0]
            month = np.datetime64(date, 'M')
            timestamp = st.subheader(month)
            animation = chosen_subset
            
            max_metric_raw = chosen_subset[chosen_subset['name'] == metric]
            max_metric = max_metric_raw['value'].max()
            max_incentive_raw = chosen_subset[chosen_subset['name'] == incentive]
            max_incentive = max_incentive_raw['value'].max()
        
            map = st.pydeck_chart(t)
    
            # Update the map for each month value
            for i in range(0, chosen_subset['date'].nunique()):
            
                new_date = chosen_subset['date'].unique()[i]
                new_month = np.datetime64(new_date, 'M')
                
                timestamp.subheader(new_month)
            
                if len(region_input) > 0:
                    selected_regions = region_input
                else:
                    selected_regions = animation.groupby('region').count().reset_index()['region'].tolist()
            
                if 'New South Wales' in selected_regions:
                    nsw = animation[animation['region'] == 'New South Wales']
                    nsw_metric = int(nsw[nsw['name'] == metric].iloc[i,6])
                    nsw_incentive = nsw[nsw['name'] == incentive].iloc[i,6]
                    states['features'][0]['properties']['COLOUR'] = 255 -((nsw_metric/max_metric) * 255)
                    states['features'][0]['properties']['HEIGHT'] = int((nsw_incentive/max_incentive * 700000))
                    
                if 'Victoria' in selected_regions:
                    vic = animation[animation['region'] == 'Victoria']
                    vic_metric = int(vic[vic['name'] == metric].iloc[i,6])
                    vic_incentive = vic[vic['name'] == incentive].iloc[i,6]
                    states['features'][1]['properties']['COLOUR'] = 255 -((vic_metric/max_metric) * 255)
                    states['features'][1]['properties']['HEIGHT'] = int((vic_incentive/max_incentive * 700000))
                    
                if 'Queensland' in selected_regions:
                    qld = animation[animation['region'] == 'Queensland']
                    qld_metric = int(qld[qld['name'] == metric].iloc[i,6])
                    qld_incentive = qld[qld['name'] == incentive].iloc[i,6]
                    states['features'][2]['properties']['COLOUR'] = 255 -((qld_metric/max_metric) * 255)
                    states['features'][2]['properties']['HEIGHT'] = int((qld_incentive/max_incentive * 700000))
                
                if 'South Australia' in selected_regions:
                    sa = animation[animation['region'] == 'South Australia']
                    sa_metric = int(sa[sa['name'] == metric].iloc[i,6])
                    sa_incentive = sa[sa['name'] == incentive].iloc[i,6]
                    states['features'][3]['properties']['COLOUR'] = 255 -((sa_metric/max_metric) * 255)
                    states['features'][3]['properties']['HEIGHT'] = int((sa_incentive/max_incentive * 700000))
                
                if 'Western Australia' in selected_regions:
                    wa = animation[animation['region'] == 'Western Australia']
                    wa_metric = int(wa[wa['name'] == metric].iloc[i,6])
                    wa_incentive = wa[wa['name'] == incentive].iloc[i,6]
                    states['features'][4]['properties']['COLOUR'] = 255 -((wa_metric/max_metric) * 255)
                    states['features'][4]['properties']['HEIGHT'] = int((wa_incentive/max_incentive * 700000))
                
                if 'Tasmania' in selected_regions:
                    tas = animation[animation['region'] == 'Tasmania']
                    tas_metric = int(tas[tas['name'] == metric].iloc[i,6])
                    tas_incentive = tas[tas['name'] == incentive].iloc[i,6]
                    states['features'][5]['properties']['COLOUR'] = 255 -((tas_metric/max_metric) * 255)
                    states['features'][5]['properties']['HEIGHT'] = int((tas_incentive/max_incentive * 700000))
                
                if 'Northern Territory' in selected_regions:
                    nt = animation[animation['region'] == 'Northern Territory']
                    nt_metric = int(nt[nt['name'] == metric].iloc[i,6])
                    nt_incentive = nt[nt['name'] == incentive].iloc[i,6]
                    states['features'][6]['properties']['COLOUR'] = 255 -((nt_metric/max_metric) * 255)
                    states['features'][6]['properties']['HEIGHT'] = int((nt_incentive/max_incentive * 700000))
                    
                if 'Australian Capital Territory' in selected_regions:
                    act = animation[animation['region'] == 'Australian Capital Territory']
                    act_metric = int(act[act['name'] == metric].iloc[i,6])
                    act_incentive = act[act['name'] == incentive].iloc[i,6]
                    states['features'][7]['properties']['COLOUR'] = 255 -((act_metric/max_metric) * 255)
                    states['features'][7]['properties']['HEIGHT'] = int((act_incentive/max_incentive * 700000))
            
                # Update the deck.gl map
                t.update()
        
                # Render the map
                map.pydeck_chart(t)
        
                # wait 0.3 second before go onto next day
                time.sleep(0.2)

### Bubble chart

if section == 'Bubble Chart':
    
    # Build y axis to be per capita measures
    y_selection = st.sidebar.selectbox(
        'Per Capita Measure:', 
        ['Loans per 100,000 people',
         'Value per person ($)'])
    
    if 'Loans per 100,000 people' in y_selection:
        y_select = 'new_loan_commitments_per_100000'
    elif 'Value per person ($)' in y_selection:
        y_select = 'value_per_person'
    
    # Build x axis to be incentives
    x_selection = st.sidebar.selectbox(
        'Incentive:', 
        ['Maximum Benefit Dollar Value',
         'Maximum Benefit as Percent of Median House Price'])
    
    if 'Maximum Benefit Dollar Value' in x_selection:
        x_select = 'max_benefit_available'
    elif 'Maximum Benefit as Percent of Median House Price' in x_selection:
        x_select = 'max_benefit_as_percent_median_house_price'

    # Build size selection from volume and value
    size_selection = st.sidebar.selectbox(
        'Size: ', 
        ['Number of New Loan Commitments for First Home Buyers',
         'Value of New Loan Commitments for First Home Buyers'])
    
    if 'Number of New Loan Commitments for First Home Buyers' in size_selection:
        size_select = 'total_new_loan_commitments'
    elif 'Value of New Loan Commitments for First Home Buyers' in size_selection:
        size_select = 'value_in_millions'
    
    # Selections
    incentive_type = st.sidebar.selectbox(
        'Type of Incentive',
        ['All','First Home Owner Grant','First Home Owner Boost','Duty Concession','Other'])
    
    option = incentive_type
    
    # Region filter
    region_input = st.sidebar.multiselect(
        'Region',
        data.groupby('region').count().reset_index()['region'].tolist())
    
    # Series filter
    series_input = st.sidebar.selectbox(
        'Series',
        ['Trend','Seasonally Adjusted','Original'])

    # Subset data
    bubble_data = data
    
    subsetter = [x_select,y_select,size_select]
    
    bubble_data = bubble_data[bubble_data['name'].isin(subsetter)]
    
    bubble_data = bubble_data[bubble_data['type'] == option]
    
    # by series
    if len(series_input) > 0:
        bubble_data = bubble_data[bubble_data['series_type'] == series_input]
    
    # by region
    if len(region_input) > 0:
        bubble_data = bubble_data[bubble_data['region'].isin(region_input)]
    
    # Pivot data to allow for bubble chart
    pivot = bubble_data.pivot_table(index = ['date','region', 'series_type','type','schemes'], columns = 'name', values = 'value').reset_index()
    
    pivot['date'] = pd.to_datetime(pivot['date']).astype(str).str.slice(0,7)
    
    # Set max axis
    y_top = pivot[y_select].max()+(pivot[y_select].max()*0.1)
    x_top = pivot[x_select].max()+(pivot[x_select].max()*0.1)
    
    # Build bubble chart
    bubble = px.scatter(pivot, x= x_select, 
                        y= y_select, 
                        size = size_select,
                        color = 'region', 
                        animation_frame = 'date', 
                        animation_group = 'region',
                        range_x = [0,x_top],
                        range_y = [0,y_top],
                        size_max = 60,
                        width = 900,
                        height = 600,
                        hover_data = {x_select:False,y_select:False,
                                      size_select:False,'schemes':True},
                        title = "Compare Per Capita Measure to Incentives Over Time")
    
    # Configure axis labels
    bubble.layout.sliders[0].currentvalue['prefix'] = 'Date: '
    bubble.layout.xaxis['title']['text'] = x_selection
    bubble.layout.yaxis['title']['text'] = y_selection
    bubble.layout.legend['title']['text'] = 'State or Territory'

    # Make bubble chart
    st.plotly_chart(bubble)
    
    # Error found when users change values during animation
    st.write('Changing values once the animation has started may cause the data to exceed the boundaries. To resolve this, reset the section.')
