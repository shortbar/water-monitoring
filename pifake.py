#pifake.py
# David R. Albrecht and Patrick Souza for Prefiat, LLC
# Contains fake gpio class objects for testing purposes

class pfio_fake:
    def __init__(self):
        self.inputs = [0 for i in range(8)]
        self.outputs = [0 for i in range(8)]
    
    def digital_read(self, pin):
        return self.inputs[pin-1]
    
    def digital_write(self, pin, value):
        self.outputs[pin-1] = value
    
    def init(self):
       self.outputs = [0 for i in self.outputs]
    