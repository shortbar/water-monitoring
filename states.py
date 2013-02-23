# states.py
# Patrick Souza for Prefiat LLC
# state objects representing each of three possible system states

class SystemState:
    def __init__(self, since, message):
        self.since = since
        self.message = message

class OKState(SystemState):
    def next(gpio_manager):
        pass

class WarningState(SystemState):
    def next(gpio_manager):
        pass

class ActionState(SystemState):
    def next(gpio_manager):
        pass
