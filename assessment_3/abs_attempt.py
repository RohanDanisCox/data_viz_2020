# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 15:47:39 2020

@author: rohan
"""
import pandasdmx as sdmx

Agency_Code = 'ABS'
Dataset_Id = 'HF'                 #'ATSI_BIRTHS_SUMM' 
ABS = sdmx.Request(Agency_Code)
data_response = ABS.data(resource_id=Dataset_Id, params={'startPeriod': '2018-11','endPeriod':'2018-11'})

data = data_response.data
msg = data_response.msg

measure = msg._elem['structure']['dimensions']['series'][0]['values']
region = msg._elem['structure']['dimensions']['series'][1]['values']
lender = msg._elem['structure']['dimensions']['series'][2]['values']
adjustment = msg._elem['structure']['dimensions']['series'][3]['values']
item = msg._elem['structure']['dimensions']['series'][4]['values']
frequency = msg._elem['structure']['dimensions']['series'][5]['values']


def flatten(l): return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]
measure2 = flatten(measure)

for x in range(0, 3):
    print("We're on time %d" % (x))


measure3 = dict(measure[1])

from collections import ChainMap
context = ChainMap({}, measure, region)
context = dict(ChainMap(measure, region))

measure.items
(measure)
dir(msg)

check = data_response.msg._elem
check_2 = data_response.msg.__elem__
check_3 = data_response.msg._elem['structure']['dimensions']['series'][1]

series = list(data.series)



series[1].key

dir(data)

key = data.key

#flow_response = ABS.dataflow('ABS') - doesn't work with ABS

test = dir(data_response.msg)

test_2 = dir(data_response.data)

                                                         
#This will result into a stacked DataFrame
df = data_response.write(data_response.data.series, parse_time=False)
df_1 = data_response.write().unstack().reset_index()
#df_2 = data_response.writer.write_dataset(data_response.data.series)
#df_3 = data_response.datastructure()

#data = (Request.to_pandas(data_response.xs('TOTAL', level='AGE', drop_level=False)))

#A flat DataFrame
data_response.write().unstack().reset_index()

