# main.py
# David R. Albrecht for Prefiat LLC
# Runs the program

import statemanager
import gpiomanager
import apimanager
import datetime
import piface.pfio as pfio_interface
import states
import sys

pfio_interface.init()
gpio_mgr = gpiomanager.GPIOManager(pfio_interface)
gis_api = apimanager.GISAPIManager()

try:
    current_state = statemanager.parse_state_file("state_file.yaml")
    current_state = current_state.next(gpio_mgr, gis_api)
except:
    current_state = states.TroubleState(datetime.datetime.now(), sys.exc_info()[0])
finally:
    current_state.set_outputs(gpio_mgr)
    statemanager.write_state_stdout(current_state)
    statemanager.write_state_file("state_file.yaml", current_state)
