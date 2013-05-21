# gpiomanager.py
# David R. Albrecht for Prefiat, LLC
# Handles setting/reading from GPIO pins on RPi

class GPIOManager:
	def __init__(self, piface_module):
		self.pfio = piface_module
		
	def _initialize_piface(self):
		self.pfio.init()
    
   	def is_floating(self):
   		self._initialize_piface()
   		if self.pfio.digital_read(0) == 0:
   			return True     # NC switch pushed open by water -> Floating
   		else:
   			return False    # NC switch in closed position -> water below switch
   
   	def set_OKState(self):
   		self._initialize_piface()
   		self.pfio.digital_write(0,1)
   		return "OKState Set"
   	
	def set_WarningState(self):
		self._initialize_piface()
   		self.pfio.digital_write(1,1)
   		return "WarningState Set"
		
	def set_ActionState(self):
	   	self._initialize_piface()
   		self.pfio.digital_write(2,1)
   		return "ActionState Set"
   	
   	def set_TroubleState(self):
   	 	self._initialize_piface()
   		self.pfio.digital_write(3,1)
   		return "TroubleState Set"
