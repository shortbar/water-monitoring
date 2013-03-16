import unittest
import statemanager
import yaml
import os
import datetime
import states
import gpiomanager

class TestGPIOManager(unittest.TestCase):
    def test_OutputPass(self):
        state_list = [states.OKState(datetime.datetime.now(),"foo"),  
                      states.WarningState(datetime.datetime.now(),"foo"), 
                      states.ActionState(datetime.datetime.now(),"foo")]
        actual = []
        gpiomgr = gpiomanager.GPIOManager()
        for i in state_list:
            actual.append(i.set_outputs(gpiomgr))
        self.assertEqual(actual, ["OKState Set", "Warning State Set", "Action State Set"], "Error Passing States") 
