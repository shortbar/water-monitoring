#apifake.py
# David R. Albrecht and Patrick Souza for Prefiat, LLC
# Contains fake API methods for testing purposes

class api_fake:
    def __init__(self):
        self.water_level = 10
    
    def read_api(self):
        return self.water_level
