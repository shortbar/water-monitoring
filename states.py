# states.py
# Patrick Souza for Prefiat LLC
# state objects representing each of three possible system states

class SystemState:
    def __init__(self, since, message):
        self.since = since
        self.message = message

class OKState(SystemState):
    def next(self, gpio_mgr):
        fs_state = gpio_mgr.is_floating()
        pass
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_OKState()

class WarningState(SystemState):
    def next(self, gpio_mgr):
        fs_state = gpio_mgr.is_floating()
        pass
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_WarningState()

class ActionState(SystemState):
    def next(self, gpio_mgr):
        fs_state = gpio_mgr.is_floating()
        pass
    def set_outputs(self, gpio_mgr):
        return gpio_mgr.set_ActionState()
