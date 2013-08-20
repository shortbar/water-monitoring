# Simulate the behavor of the Plum Creek API to facilitate testing at Franciscan.
# Simple rule: During AM hours CDT, "api" will read 14 feet, 16 feet during PM hours
# (14ft 05:00-16:59:59 UTC, 16ft 17:00-04:59:59)
class TimeSimulatedAPIManager:
    def __init__(self):
        pass
    
    def get_plum_creek_gage_height_ft(self):
        hour = datetime.datetime.now().hour
        
        if hour > 4 and hour < 17:
            return 14
        else:
            return 16
