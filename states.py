# states.py
# Patrick Souza for Prefiat LLC
# state objects representing each of three possible system states

import datetime

class SystemState(object):
    def __init__(self, last_checked, since, api_faults, message):
        '''Default initializer used when a check executes correctly'''
        self.last_checked = last_checked
        self.since = since
        self.api_faults = api_faults
        self.message = message
        self.allowable_faults = 30
        
    def __eq__(self, other):
        return type(self) == type(other)

    def api_read_failure(self, message):
        return self.__class__(self.last_checked, self.since, self.api_faults + 1, message)
        
    def dwell(self, message):
        return self.__class__(self.last_checked, self.since, self.api_faults, message)
        
    def next(self, gpio_mgr, api_mgr):
        is_floating = gpio_mgr.is_floating()
        
        if self.should_dwell():
            return self.dwell("Still {}. Floating: {}".format(__name__, is_floating))
        
        try:
            gage_height_feet = api_mgr.get_plum_creek_gage_height_ft()
            return self.next_no_dwell(is_floating, gage_height_feet)
        except:
            if self.api_faults + 1 > self.allowable_faults:
                return TroubleState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                    "API read failure in {}".format(__name__))
            else:
                return self.api_read_failure("{}->{} (api fault)".format(__name__, __name__))
        
    def should_dwell(self):
        return (datetime.datetime.now() - self.last_checked) < datetime.timedelta(seconds=self.dwell_time_s)

    def stay_after_check(self, is_floating, gage_height_feet):
        return self.__class__(datetime.datetime.now(), self.since, 0, ("{}->{}. Plum Creek water level at {} " +
            "feet, floating: {}").format(__name__, __name__, gage_height_feet, is_floating))
        
class OKState(SystemState):
    def __init__(self, last_checked, since, api_faults, message):
        super(OKState, self).__init__(last_checked, since, api_faults, message)
        self.dwell_time_s = 3600
        
    def next_no_dwell(self, is_floating, gage_height_feet):
        if gage_height_feet >= 15.3:
            return WarningState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                "OK->Warning. Plum Creek water level at {} feet, floating: {}".format(\
                gage_height_feet, is_floating))
        else:
            if is_floating:
                return DrainCloggedState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                    "OK->DrainClogged. Plum Creek water level at {} feet, floating: {}".format(\
                    gage_height_feet, is_floating))
            else:
                return self.stay_after_check(is_floating, gage_height_feet)
                
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_OKState()

class WarningState(SystemState):
    def __init__(self, last_checked, since, api_faults, message):
        super(WarningState, self).__init__(last_checked, since, api_faults, message)
        self.dwell_time_s = 900
        
    def next_no_dwell(self, is_floating, gage_height_feet):
        if is_floating:
            if gage_height_feet >= 15.3:
                return ActionState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                    "Warning->Action. Float switch is either raised or out of order. Plum Creek water " + \
                    "level at {} feet, floating: {}".format(gage_height_feet, is_floating))
            else:
                return DrainCloggedState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                    "Warning->DrainClogged. Plum Creek water level at {} feet, floating: {}".format(\
                    gage_height_feet, is_floating))
        else:
            if gage_height_feet <= 15.0:
                return OKState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                    "Warning->OK. Plum Creek water level at {} feet, floating: {}".format(
                    gage_height_feet, is_floating))
            else:
                return self.stay_after_check(is_floating, gage_height_feet)

    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_WarningState()

class ActionState(SystemState):
    def __init__(self, last_checked, since, api_faults, message):
        super(ActionState, self).__init__(last_checked, since, api_faults, message)
        self.dwell_time_s = 900

    def next_no_dwell(self, is_floating, gage_height_feet):
        if gage_height_feet <= 15:
            if is_floating:
                return DrainCloggedState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                    "Action->DrainClogged. Plum Creek water level at {} feet, floating: {}".format(\
                    gage_height_feet, is_floating))
            else:
                return OKState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                    "Action->OK. Plum Creek water level at {} feet, floating: {}".format(\
                    gage_height_feet, is_floating))
        else:
            return self.stay_after_check(is_floating, gage_height_feet)
            
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_ActionState()

class DrainCloggedState(SystemState):
    def __init__(self, last_checked, since, api_faults, message):
        super(DrainCloggedState, self).__init__(last_checked, since, api_faults, message)
        self.dwell_time_s = 3600
        
    def next_no_dwell(self, is_floating, gage_height_feet):
        if gage_height_feet >= 15.3:
            return WarningState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                "Clog->Warning. Float switch appears stuck but proceeding to Warning State. " +
                "Plum Creek water level at {} feet, floating: {}".format(gage_height_feet, is_floating))
        else:
            if is_floating:
                return self.stay_after_check(is_floating, gage_height_feet)
            else:
                return OKState(datetime.datetime.now(), datetime.datetime.now(), 0, \
                    "Clog->OK. Plum Creek water level at {} feet, floating: {}".format(\
                    gage_height_feet, is_floating))
                    
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_DrainCloggedState()

# State Cycle Test -- checks whether we can go through all the states.
class StateCycleOK(SystemState):
    def next(self, gpio_mgr, api_mgr):
        return StateCycleWarning(datetime.datetime.now(), datetime.datetime.now(), 0, \
            'State cycle test, OK->Warning')
    
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_OKState()

class StateCycleWarning(SystemState):
    def next(self, gpio_mgr, api_mgr):
        if gpio_mgr.is_floating():
            return StateCycleAction(datetime.datetime.now(), datetime.datetime.now(), 0, \
                'State cycle test, switch floating, Warning->Action')
        else:
            return StateCycleWarning(datetime.datetime.now(), datetime.datetime.now(), 0, \
                'State cycle test, staying in warning')
    
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_WarningState()
    
class StateCycleAction(SystemState):
    def next(self, gpio_mgr, api_mgr):
        if gpio_mgr.is_floating():
            return StateCycleAction(datetime.datetime.now(), datetime.datetime.now(), 0, \
                'State cycle test, switch floating, staying in action')
        else:
            return StateCycleOK(datetime.datetime.now(), datetime.datetime.now(), 0, \
                'State cycle test, in Action, moving to OK')
    
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_ActionState()

# System trouble
class TroubleState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        return self     # Trouble is a trap state; stay in it until we're manually reset
        
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_TroubleState()
