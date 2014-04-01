# test_gpiomanager.py
# David R. Albrecht and Patrick Souza for Prefiat, LLC
# Checks that gpio_manager sets output pins according to spec

import unittest
import datetime
import states
import gpiomanager
import pifake

class TestGPIOManager(unittest.TestCase):
    def setUp(self):
        self.pfio_interface = pifake.pfio_fake()
        self.gpiomgr = gpiomanager.GPIOManager(self.pfio_interface)
        
    def test_AllClearOutput(self):
        system_state = states.OKState(datetime.datetime.now(), datetime.datetime.now(), 0, "foo")
        system_state.set_outputs(self.gpiomgr)
        
        self.assertEqual(self.pfio_interface.read_output(), 0x11, "Incorrect output for all clear state")
    
    def test_WarningOutput(self):
        system_state = states.WarningState(datetime.datetime.now(), datetime.datetime.now(), 0, "foo")
        system_state.set_outputs(self.gpiomgr)
        
        self.assertEqual(self.pfio_interface.read_output(), 0x22, "Incorrect output for warning state")
        
    def test_ActionOutput(self):
        system_state = states.ActionState(datetime.datetime.now(), datetime.datetime.now(), 0, "foo")
        system_state.set_outputs(self.gpiomgr)
        
        self.assertEqual(self.pfio_interface.read_output(), 0x44, "Incorrect output for action state")
        
    def test_SystemTroubleOutput(self):
        system_state = states.TroubleState(datetime.datetime.now(), datetime.datetime.now(), 0, "foo")
        system_state.set_outputs(self.gpiomgr)
        
        self.assertEqual(self.pfio_interface.read_output(), 0x78, "Incorrect output for system trouble state")

    def test_clogged_state_sets_output_correctly(self):
        system_state = states.DrainCloggedState(datetime.datetime.now(), datetime.datetime.now(), 0, "foo")
        system_state.set_outputs(self.gpiomgr)
        
        self.assertEqual(self.pfio_interface.read_output(), 0x66, "Incorrect output for drain clogged state")
