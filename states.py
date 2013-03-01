# states.py
# Patrick Souza for Prefiat LLC
# state objects representing each of three possible system states

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
    def next(gpio_manager):
        pass

class WarningState(SystemState):
    def next(gpio_manager):
        pass

class ActionState(SystemState):
    def next(gpio_manager):
        pass
