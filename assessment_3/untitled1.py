# -*- coding: utf-8 -*-
"""
Created on Sat May  9 07:48:32 2020

@author: rohan
"""

import pandasdmx as sdmx

estat = sdmx.Request('ESTAT')

metadata = estat.datastructure('DSD_une_rt_a')

resp = estat.data('une_rt_a',key={'GEO': 'EL+ES+IE'},params={'startPeriod': '2007'})

data = resp.to_pandas().xs('Y15-74', level='AGE',axis=1, drop_level=False)

data = resp.write()

data2 = resp.write().xs('Y15-74', level='AGE',axis=1, drop_level=False)

test = sdmx.to_pandas(resp)

dir(sdmx)
help(sdmx)


url = 'http://stat.data.abs.gov.au/sdmx-json/data/BOP/1.170.20.Q/all?detail=Full&dimensionAtObservation=AllDimensions&startPeriod=2015-Q2'
test = sdmx.Request.get(url = url)


