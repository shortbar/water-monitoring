import unittest
import statemanager
import yaml
import os
import datetime
import states
import gpiomanager
import apifake
import pifake

class testOKStateTransitions(unittest.TestCase):
    
    def setUp(self):
        self.api_mgr = apifake.api_fake()
        self.pfio_interface_fake = pifake.pfio_fake()
        self.gpio_mgr = gpiomanager.GPIOManager(self.pfio_interface_fake)
    
    def test_OKState_to_OKState(self):
        self.api_mgr.water_level = 10
        current_state = states.OKState(datetime.datetime.now(), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.OKState, "Error maintaining OKState")
        
    def test_OKState_to_WarningState(self):
        self.api_mgr.water_level = 16
        current_state = states.OKState(datetime.datetime.now(), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.WarningState, "Error in OKState -> WarningState transition")
        