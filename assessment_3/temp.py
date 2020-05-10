# -*- coding: utf-8 -*-
"""
Extracting and testing ABS data
"""

from pandasdmx import Request

Agency_Code = 'ABS'
Dataset_Id = 'HF'                 
ABS = Request(Agency_Code)
data_response = ABS.data(resource_id=Dataset_Id, params={'startPeriod': '2018-11',
                                                         'endPeriod':'2018-11'})

data = data_response.to_pandas()
data = cat_msg.to_pandas()

#flow_response = ABS.dataflow('ABS') - doesn't work with ABS

help(data_response)
help(data_response.__dict__)


### looking at website https://pandasdmx.readthedocs.io/en/v0.3.0/usage.html
cat_res = data_response
cat_msg = cat_res.msg
categories = dir(cat_msg)
cs = cat_msg.categoryschemes

data = data_response.msg.data
type(data)
dir(data)
data.dim_at_obs
series_l = list(data.series)

series_l[5].key
set(s.key.FREQUENCY for s in data.series)

frame = data_response.write()
frame.index

frame.columns

test = frame.stack(0)
test_2 = frame.unstack()
test_3 = test_2.reset_index()

df = data_response.write(data_response.data.series, parse_time=False)
df_1 = data_response.write().unstack().reset_index()

test_3.replace(check_3)
### Found the things I am interested in.
check = data_response.__dict__
check_2 = data_response.msg.__elem__
check_3 = data_response.msg._elem['structure']['dimensions']['series'][1]

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








##### TRYING INSTEAD WITH PANDAS - can't get it to work
import urllib
import pandas as pd

url = 'http://stat.data.abs.gov.au/sdmx-json/data/BOP/1.170.20.Q/all?detail=Full&dimensionAtObservation=AllDimensions&startPeriod=2015-Q2'
json_url = urllib.urlopen(url)

help(urllib)
