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
import os



pfio_interface.init()
gpio_mgr = gpiomanager.GPIOManager(pfio_interface)
gis_api = apimanager.GISAPIManager()

try:
    # Ensure enough space on the root device of the volume
    st = os.statvfs('/')
    free_space_mb = st.f_bavail * st.f_frsize / 1024 / 1024
    if free_space_mb < 128:
        raise Exception("Less than 128MB disk space free, raising system trouble state")
    
    current_state = statemanager.parse_state_file("state_file.yaml")
    current_state = current_state.next(gpio_mgr, gis_api)
except:
    current_state = states.TroubleState(datetime.datetime.now(), datetime.datetime.now(), 0, sys.exc_info()[0])
finally:
    current_state.set_outputs(gpio_mgr)
    statemanager.write_state_stdout(current_state)
    statemanager.write_state_file("state_file.yaml", current_state)
