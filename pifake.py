#pifake.py
# David R. Albrecht and Patrick Souza for Prefiat, LLC
# Contains fake gpio class objects for testing purposes

import copy

class pfio_fake:
    def __init__(self):
        self.input_pins = 0xff
        self.output_pins = 0xff
    
    def init(self):
       self.output_pins = 0xff
    
    def write_output(self, data):
        self.output_pins = data
    
    def digital_write(self, pin_number, value):
        pin_bit_mask = pfio_fake.get_pin_bit_mask(pin_number)
        
        if value:
            self.output_pins = self.output_pins | pin_bit_mask
        else:
            self.output_pins = self.output_pins & ~pin_bit_mask
    
    def read_output(self):
        return self.output_pins
    
    def digital_read(self, pin_number):
        pin_bit_mask = pfio_fake.get_pin_bit_mask(pin_number)
        result = self.input_pins & pin_bit_mask

        # is this correct? -thomas preston
        if result:
            return 1
        else:
            return 0
    
    def set_floating(self):
        # Switch is NC to set floating -> clear the bit
        pin_bit_mask = 0x01
        self.input_pins = self.input_pins & ~pin_bit_mask
    
    def clear_floating(self):
        # NC switch. Clear floating -> make the bit high
        pin_bit_mask = 0x01
        self.input_pins = self.input_pins | pin_bit_mask
        
    @staticmethod
    def get_pin_bit_mask(pin_number):
        """Translates a pin number to pin bit mask. First pin is pin0."""
        if pin_number > 7 or pin_number < 0:
            raise PinRangeError("Specified pin number (%d) out of range." % pin_number)
        else:
            return 1 << (pin_number)
