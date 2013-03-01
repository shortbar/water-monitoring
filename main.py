# main.py
# David R. Albrecht for Prefiat LLC
# Runs the program

import statemanage
import gpiomanager

gpio_mgr = gpiomanager.GPIOManager()
gis_api = gisapi.GISAPI()

try:
	current_state = statemanager.parse_state_file()
	current_state = current_state.next(gpio_mgr)
	current_state.set_outputs(gpio_mgr)
	
	statemanager.save(current_state)
except:
	gpio_mgr.set_trouble()
