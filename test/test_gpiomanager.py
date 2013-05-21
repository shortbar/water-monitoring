# test_gpiomanager.py
# David R. Albrecht and Patrick Souza for Prefiat, LLC
# Checks that gpio_manager sets output pins according to spec

import unittest
import statemanager
import yaml
import os
import datetime
import states
import gpiomanager
import pifake

class TestGPIOManager(unittest.TestCase):
    def test_OutputPass(self):
        pfio_interface = pifake.pfio_fake()
        state_list = [states.OKState(datetime.datetime.now(),"foo"),  
                      states.WarningState(datetime.datetime.now(),"foo"), 
                      states.ActionState(datetime.datetime.now(),"foo"),
                      states.TroubleState(datetime.datetime.now(),"foo")]
                      
        gpiomgr = gpiomanager.GPIOManager(pfio_interface)
        for i in state_list:
            i.set_outputs(gpiomgr)
            print i, pfio_interface.outputs
            self.assertEqual(pfio_interface.outputs[state_list.index(i)], 1, "Error Setting {}".format(i)) 
