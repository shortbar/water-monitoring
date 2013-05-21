# gpiomanager.py
# David R. Albrecht for Prefiat, LLC
# Gets the water height using the GIS API

import urllib3
import json

class GISAPIManager:
    def __init__(self):
        # Get usgs site 05536162 (Plum Creek), parameter 00065 (gage height)
        self.usgs_url = "http://waterservices.usgs.gov/nwis/iv/?format=json&site=05536162&parameterCd=00065"
	
    def get_plum_creek_gage_height_ft(self):
        http = urllib3.PoolManager()
        try:
            r = http.request('GET', self.usgs_url)
        except:
            # TODO: handle API access error
            pass
        
        if r.status != 200:
            # TODO: Handle API access error
            pass
        
        gis_response = json.loads(r.data)
        try:
            height_ft_string = gis_response['value']['timeSeries'][0]['values'][0]['value'][0]['value']
            height_ft_float = float(height_string)
        except:
            # TODO: handle invalid format error
            # TODO: Handle invalid conversion error
            pass
        
        return height_ft_float
