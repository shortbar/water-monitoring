# gpiomanager.py
# David R. Albrecht for Prefiat, LLC
# Handles setting/reading from GPIO pins on RPi

import piface.pfio as pfio

class GPIOManager:
	def __init__(self):
	    pass
    
    def _initialize_piface(self):
    	pfio.init()
    
   	def is_floating(self):
   		self._initialize_piface()
   		state_1 = pfio.digital_read(1):
   		if state_1 == 0 
   			return True
   		else:
   			return False
   
   	def set_OKState(self):
   		self._initialize_piface()
   		pfio.digital_write(1,1)
   		return "OKState Set"
   	
	def set_WarningState(self):
		self._initialize_piface()
   		pfio.digital_write(2,1)
   		return "WarningState Set"
		
	def set_ActionState(self):
	   	self._initialize_piface()
   		pfio.digital_write(3,1)
   		return "ActionState Set"
   	
   	def set_TroubleState(self):
   	 	self._initialize_piface()
   		pfio.digital_write(4,1)
   		return "TroubleState Set"
    