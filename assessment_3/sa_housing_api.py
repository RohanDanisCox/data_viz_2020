# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 08:51:18 2020

@author: rohan
"""

import urllib
url = 'https://data.sa.gov.au/data/api/3/action/datastore_search?resource_id=fec742c1-c846-4343-a9f1-91c729acd097&limit=5&q=title:jones'  
fileobj = urllib.urlopen(url)
print fileobj.read()
