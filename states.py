# states.py
# Patrick Souza for Prefiat LLC
# state objects representing each of three possible system states
import datetime

class SystemState:
    def __init__(self, since, message):
        self.since = since
        self.message = message
        
    def __eq__(self, other):
        if type(self) == type(other):
            if self.since == other.since:
                if self.message == other.message:
                    if self.__class__ == other.__class__:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
        
class OKState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        fs_state = gpio_mgr.is_floating()
        api_state = api_mgr.read_api()
        if api_state < 15.3:
            return OKState(datetime.datetime.now(), "Current State is: Okay. Plum Creek water level at {} meters".format(api_state))
        elif api_state >= 15.3:
            return WarningState(datetime.datetime.now(), "Current state is: Warning. Plum Creek water level at {} meters".format(api_state))
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_OKState()

class WarningState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        fs_state = gpio_mgr.is_floating()
        api_state = api_mgr.read_api()
        pass
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_WarningState()

class TroubleState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        fs_state = gpio_mgr.is_floating()
        api_state = api_mgr.read_api()
        pass
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_TroubleState()

class ActionState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        fs_state = gpio_mgr.is_floating()
        api_state = api_mgr.read_api()
        pass
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_ActionState()

class TroubleState(SystemState):
    def next(self, gpio_mgr, api_mgr):
        fs_state = gpio_mgr.is_floating()
        api_state = api_mgr.read_api()
        pass  
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_TroubleState()
    
