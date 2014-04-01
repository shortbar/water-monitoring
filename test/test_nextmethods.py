import unittest
import statemanager
import yaml
import os
import datetime
import states
import gpiomanager
import apifake
import pifake

class TestSystemStateTransitions(unittest.TestCase):
    def setUp(self):
        self.api_mgr = apifake.api_fake()
        self.pfio_interface_fake = pifake.pfio_fake()
        self.gpio_mgr = gpiomanager.GPIOManager(self.pfio_interface_fake)

    def test_dwells_when_under_time(self):
        old_state = states.OKState(datetime.datetime.now() - datetime.timedelta(0, 60, 0), \
            datetime.datetime.now(), 0, "foo")
        new_state = old_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(new_state, states.OKState, "Error in maintaining OKState by insufficient time interval")
        self.assertEqual(old_state.last_checked, new_state.last_checked)

    def test_calls_next_when_over_time(self):
        self.api_mgr.water_level = 10
        old_state = states.OKState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), \
            datetime.datetime.now(), 0, "foo")
        new_state = old_state.next(self.gpio_mgr, self.api_mgr)
        self.assertIsInstance(new_state, states.OKState, "OKState did not return a new instance of itself")
        self.assertNotEqual(old_state.last_checked, new_state.last_checked)

class TestOKStateTransitions(unittest.TestCase):
    def setUp(self):
        self.start_state = states.OKState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), \
            datetime.datetime.now(), 0, "foo")
            
    def test_not_floating_api_reads_low(self):
        gage_height_feet = 10
        is_floating = False
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.OKState, "Failure to maintain OKState")
    
    def test_not_floating_but_api_reads_high(self):
        gage_height_feet = 16
        is_floating = False
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.WarningState, "Failure to proceed to warning state")
            
    def test_floating_but_api_reads_low(self):
        gage_height_feet = 10
        is_floating = True
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.DrainCloggedState, "Failure to enter drain clogged from OKState")
        
    def test_floating_and_api_reads_high(self):
        gage_height_feet = 16
        is_floating = True
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.WarningState, "Failure to enter warning state from OKState")    
    
class TestWarningStateTransitions(unittest.TestCase):
    def setUp(self):
        self.start_state = states.WarningState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), \
            datetime.datetime.now(), 0, "foo")

    def test_not_floating_api_reading_very_low(self):
        gage_height_feet = 5
        is_floating = False
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.OKState, "Failure to return to OKState from WarningState")
    
    def test_not_floating_api_reading_low(self):
        gage_height_feet = 15
        is_floating = False
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.OKState, "Failure to return to OKState from WarningState")
        
    def test_not_floating_api_reading_high(self):
        gage_height_feet = 16
        is_floating = False
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.WarningState, "Failure to maintain warning from warning")
    
    def test_floating_but_api_reading_low(self):
        gage_height_feet = 10
        is_floating = True
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.DrainCloggedState, "Failure to enter DrainCloggedState from Warning")
    
    def test_floating_api_reading_high(self):
        gage_height_feet = 16
        is_floating = True
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.ActionState, "Failure to enter Action from Warning")

class TestActionStateTransitions(unittest.TestCase):
    def setUp(self):
        self.start_state = states.ActionState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), \
            datetime.datetime.now(), 0, "foo")
    
    def test_not_floating_api_low(self):
        gage_height_feet = 10
        is_floating = False
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.OKState, "Failure to return to OK from Action")
        
    def test_not_floating_api_high(self):
        gage_height_feet = 16
        is_floating = False
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.ActionState, "Failure to stay in Action")
    
    def test_floating_api_low(self):
        gage_height_feet = 10
        is_floating = True
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.DrainCloggedState, "Failure to enter DrainCloggedState from Action")
    
    def test_foating_api_high(self):
        gage_height_feet = 16
        is_floating = True
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.ActionState, "Failure to maintain Action from Action")

class TestDrainCloggedStateTransitions(unittest.TestCase):
    def setUp(self):
        self.start_state = states.DrainCloggedState(datetime.datetime.now() - datetime.timedelta(0, 4000, 0), \
            datetime.datetime.now(), 0, "foo")
    
    def test_not_floating_api_low(self):
        gage_height_feet = 10
        is_floating = False
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.OKState, "Failure to return to OKState from drain clog")
    
    def test_not_floating_api_high(self):
        gage_height_feet = 16
        is_floating = False
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.WarningState, "Failure to proceed to warning from drain clog")
    
    def test_floating_api_low(self):
        gage_height_feet = 10
        is_floating = True
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.DrainCloggedState, "Failure to maintain DrainCloggedState")
    
    def test_floating_api_high(self):
        gage_height_feet = 16
        is_floating = True
        end_state = self.start_state.next_no_dwell(is_floating, gage_height_feet)
        self.assertIsInstance(end_state, states.WarningState, "Failure to proceed to warning with drain clog")
