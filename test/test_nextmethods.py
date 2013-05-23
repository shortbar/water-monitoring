import unittest
import statemanager
import yaml
import os
import datetime
import states
import gpiomanager
import apifake
import pifake

class TestOKStateTransitions(unittest.TestCase):
    
    def setUp(self):
        self.api_mgr = apifake.api_fake()
        self.pfio_interface_fake = pifake.pfio_fake()
        self.gpio_mgr = gpiomanager.GPIOManager(self.pfio_interface_fake)
    
    def tearDown(self):
        pass
    
    def test_OKState_to_OKState(self):
        self.api_mgr.water_level = 10
        current_state = states.OKState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.OKState, "Error maintaining OKState")
        
    def test_OKState_to_WarningState(self):
        self.api_mgr.water_level = 16
        current_state = states.OKState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.WarningState, "Error in OKState -> WarningState transition")
        
    def test_BelowTimeThreshold(self):
        self.api_mgr.water_level = 16
        current_state = states.OKState(datetime.datetime.now() - datetime.timedelta(0, 60, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.OKState, "Error in maintaining OKState by insufficient time interval")

class TestWarningStateTransitions(unittest.TestCase):
    
    def setUp(self):
        self.api_mgr = apifake.api_fake()
        self.pfio_interface_fake = pifake.pfio_fake()
        self.gpio_mgr = gpiomanager.GPIOManager(self.pfio_interface_fake)
        
    def test_WarningState_to_WarningState(self):
        self.api_mgr.water_level = 16
        self.pfio_interface_fake.clear_floating()
        current_state = states.WarningState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.WarningState, "Error maintaining Warning State") 
    
    def test_WarningState_to_OKState(self):
        self.api_mgr.water_level = 10
        current_state = states.WarningState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.OKState, "Error in WarningState -> OKState transition")
        
    def test_WarningState_to_ActionState(self):
        self.api_mgr.water_level = 16
        self.pfio_interface_fake.set_floating()
        current_state = states.WarningState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.ActionState, "Error in WarningState -> ActionState transition")
        
    def test_BelowTimeThreshold(self):
        self.api_mgr.water_level = 16
        self.pfio_interface_fake.set_floating()
        current_state = states.WarningState(datetime.datetime.now() - datetime.timedelta(0, 400, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.WarningState, "Error in time difference check.")              

class TestActionStateTransitions(unittest.TestCase):
    
    def setUp(self):
        self.api_mgr = apifake.api_fake()
        self.pfio_interface_fake = pifake.pfio_fake()
        self.gpio_mgr = gpiomanager.GPIOManager(self.pfio_interface_fake)
        
    def test_ActionState_to_ActionState(self):
        self.api_mgr.water_level = 16
        current_state = states.ActionState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.ActionState, "Error maintaining Action State")
    
    def test_ActionState_to_OKState(self):
        self.api_mgr.water_level = 10
        current_state = states.ActionState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.OKState, "Error in ActionState -> OKState transition")
    
    def test_BelowTimeThreshold(self):
        self.api_mgr.water_level = 10
        current_state = states.ActionState(datetime.datetime.now() - datetime.timedelta(0, 400, 0), "foo")
        current_state = current_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(current_state, states.ActionState, "Error in timedelta check")