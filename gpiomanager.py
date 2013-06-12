# gpiomanager.py
# David R. Albrecht for Prefiat, LLC
# Handles setting/reading from GPIO pins on RPi

class GPIOManager:
    def __init__(self, piface_module):
        self.pfio = piface_module
    
    def is_floating(self):
        if self.pfio.digital_read(0) == 0:
            return True     # NC switch pushed open by water -> Floating
        else:
            return False    # NC switch in closed position -> water below switch
   
    def set_OKState(self):
        self.pfio.write_output(0x11)
        return 0x11
   	
    def set_WarningState(self):
        self.pfio.write_output(0x22)
        return 0x22
		
    def set_ActionState(self):
        self.pfio.write_output(0x44)
        return 0x44
   	
    def set_TroubleState(self):
        self.pfio.write_output(0x78)
        return 0x78
