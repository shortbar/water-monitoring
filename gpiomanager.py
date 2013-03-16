# gpiomanager.py
# David R. Albrecht for Prefiat, LLC
# Handles setting/reading from GPIO pins on RPi

class GPIOManager:
	def __init__(self):
	    pass
    
   	def is_floating(self):
   		return True
   
   	def set_OKState(self):
   		#piface.setstate(0)
   		return "OKState Set"
	def set_WarningState(self):
		return "Warning State Set"
	def set_ActionState(self):
		return "Action State Set"
   	def set_TroubleState(self):
   		pass
    