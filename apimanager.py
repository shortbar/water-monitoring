# gpiomanager.py
# David R. Albrecht for Prefiat, LLC
# Gets the water height using the GIS API

import urllib3
import json
import datetime

class GISAPIManager:
    def __init__(self):
        # Get usgs site 05536162 (Plum Creek), parameter 00065 (gage height)
        self.usgs_url = "http://waterservices.usgs.gov/nwis/iv/?format=json&site=05536162&parameterCd=00065"
	
    def get_plum_creek_gage_height_ft(self):
        http = urllib3.PoolManager()
        try:
            r = http.request('GET', self.usgs_url)
        except:
            print "Network/transport error connecting to USGS API"
            raise
        
        if r.status != 200:
            print "Error: non-200 return code from USGS API"
            raise Exception("Non-200 return code from USGS API")
        
        gis_response = json.loads(r.data)
        try:
            height_ft_string = gis_response['value']['timeSeries'][0]['values'][0]['value'][0]['value']
            height_ft_float = float(height_ft_string)
        except:
            print "Error: Data format / conversion error"
            raise
        
        return height_ft_float
