# main.py
# David R. Albrecht for Prefiat LLC
# Runs the program

import statemanager
import gpiomanager
import apimanager
import datetime
import piface.pfio as pfio_interface
import states

# where does the piface get initialized?
pfio_interface.init()
gpio_mgr = gpiomanager.GPIOManager(pfio_interface)
gis_api = apimanager.GISAPIManager()

try:
	current_state = statemanager.parse_state_file()
	current_state = current_state.next(gpio_mgr, apimanager)
	current_state.set_outputs(gpio_mgr)
	statemanager.write_state_file("state_file.yaml", current_state)
except:
	current_state = states.TroubleState(datetime.datetime.now(), "Exeption Raised")
	current_state.set_outputs(gpio_mgr)
	statemanager.write_state_file("state_file.yaml", current_state)
