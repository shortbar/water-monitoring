# states.py
# Patrick Souza for Prefiat LLC
# state objects representing each of three possible system states

import datetime

class SystemState:
    def __init__(self, since, message):
        self.since = since
        self.message = message
        
    def __eq__(self, other):
        return (type(self) == type(other) and self.since == other.since and self.message == other.message and self.__class__ == other.__class__)
        
class OKState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        is_floating = gpio_mgr.is_floating()
        gage_height_feet = api_mgr.get_plum_creek_gage_height_ft()
        d_time = (datetime.datetime.now() - self.since).total_seconds()
        if d_time < 3600:
            return OKState(datetime.datetime.now(), "Current State is: Okay. Plum Creek water level at {} feet".format(gage_height_feet))
        elif gage_height_feet < 15.3:
            return OKState(datetime.datetime.now(), "Current State is: Okay. Plum Creek water level at {} feet".format(gage_height_feet))
        elif gage_height_feet >= 15.3:
            return WarningState(datetime.datetime.now(), "Current state is: Warning. Plum Creek water level at {} feet".format(gage_height_feet))
        
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_OKState()

class WarningState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        is_floating = gpio_mgr.is_floating()
        gage_height_feet = api_mgr.get_plum_creek_gage_height_ft()
        d_time = (datetime.datetime.now() - self.since).total_seconds()
        if d_time < 900:
            return WarningState(datetime.datetime.now(), "Current State is: Warning. Plum Creek water level at {} feet".format(gage_height_feet))
        elif is_floating == True and gage_height_feet >= 15.3:
            return ActionState(datetime.datetime.now(), "Current State is: Action. Float switch is either raised or out of order. Plum Creek water level at {} feet".format(gage_height_feet))
        elif is_floating == False and gage_height_feet >= 15.3:
            return WarningState(datetime.datetime.now(), "Current State is: Warning. Plum Creek water level at {} feet".format(gage_height_feet))
        elif gage_height_feet < 15.3:
            return OKState(datetime.datetime.now(), "Current State is: Okay. Plum Creek water level at {} feet".format(gage_height_feet))
        
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_WarningState()

class TroubleState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        is_floating = gpio_mgr.is_floating()
        gage_height_feet = api_mgr.get_plum_creek_gage_height_ft()
        pass
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_TroubleState()

class ActionState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        is_floating = gpio_mgr.is_floating()
        gage_height_feet = api_mgr.get_plum_creek_gage_height_ft()
        d_time = (datetime.datetime.now() - self.since).total_seconds()
        if d_time < 900:
            return ActionState(datetime.datetime.now(), "Current State is: Action. Plum Creek water level at {} feet. Float switch raised: {}".format(gage_height_feet, is_floating))
        elif gage_height_feet >= 15:
            return ActionState(datetime.datetime.now(), "Current State is: Action. Plum Creek water level at {} feet. Float switch raised: {}".format(gage_height_feet, is_floating))
        elif gage_height_feet < 15:
            return OKState(datetime.datetime.now(), "Current State is: Okay. Plum Creek water level at {} feet".format(gage_height_feet))
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_ActionState()

class TroubleState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        is_floating = gpio_mgr.is_floating()
        gage_height_feet = api_mgr.get_plum_creek_gage_height_ft()
        return self     # Trouble is a trap state; stay in it until we're manually reset
        
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_TroubleState()
