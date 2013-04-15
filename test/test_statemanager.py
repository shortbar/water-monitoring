# test_stateread.py
# Patrick Souza <souza.patrick@gmail.com> for Prefiat LLC
# Test methods for the statread.py method: reading system state.

import unittest
import statemanager
import yaml
import os
import datetime
import states

class TestStateWrite(unittest.TestCase):
    def setUp(self):
        self.test_file_name = "test/tmp/System_State.yaml"
        self.okay_mock = states.OKState(datetime.datetime.now(), "Everything will be fine")
        pass
    
    def tearDown(self):
        pass
    
    def test_OpenFile(self):
        actual = statemanager._open_file_for_save(self.test_file_name)
        self.assertIs(type(actual), file, "Error writing file")
    
    def test_StateWrite(self):
        statemanager.write_state_file(self.test_file_name, self.okay_mock)
        actual = open(self.test_file_name, 'r')
        self.assertIs(type(actual), file, "Error writing file")
    
    def test_RoundTrip(self):
        statemanager.write_state_file(self.test_file_name, self.okay_mock)
        actual = statemanager.parse_state_file(self.test_file_name)
        self.assertEqual(actual, self.okay_mock)
    
class TestStateRead(unittest.TestCase):
    def setUp(self):
        
        #Create mock files for testing
        self.mock_file_dict = { "empty_mock.yaml" : "",
                                "normal_mock.yaml" :    "!!python/object:states.OKState {message: No Message, since: !!timestamp '2013-02-28\n    20:29:53.696503'}\n",
                                "warning_mock.yaml":    "!!python/object:states.WarningState {message: No Message, since: !!timestamp '2013-02-28\n    20:29:53.696503'}\n",
                                "action_mock.yaml":    "!!python/object:states.ActionState {message: No Message, since: !!timestamp '2013-02-28\n    20:29:53.696503'}\n",
                                "trash_mock.yaml":   """a;slkdfj;laskjdf;akj"""
                                }
        for i in self.mock_file_dict.iterkeys():
            f = open(i, "w+")
            f.write(self.mock_file_dict[i])
            f.close                
                    
    def test_FileMissing(self):
        self.assertRaises(statemanager.MissingStateFileError, statemanager._get_file_handle, "nonexistent.yaml")
        
    def test_FileNotMissing(self):  
        actual = statemanager._get_file_handle("empty_mock.yaml")
        self.assertIs(type(actual), file, "File is missing")
        
    def test_Recovers_OK_State(self):
        actual = statemanager.parse_state_file("normal_mock.yaml")
        self.assertIsInstance(actual, states.OKState, "Error Recovering OK State")
        
    def test_Recovers_Warning_State(self):
        actual = statemanager.parse_state_file("warning_mock.yaml")
        self.assertIsInstance(actual, states.WarningState, "Error Recovering Warning State")
    
    def test_Recovers_Alert_State(self):
        actual = statemanager.parse_state_file("action_mock.yaml")
        self.assertIsInstance(actual, states.ActionState, "Error Recovering Action State")
    
    def test_Recovers_correct_date(self):
        actual = statemanager.parse_state_file("normal_mock.yaml").since
        expected = datetime.datetime(2013, 2, 28, 20, 29, 53, 696503)
        self.assertEqual(actual, expected, "Unexpected datetime")
    
    def test_Recovers_correct_message(self):
        actual = statemanager.parse_state_file("normal_mock.yaml").message
        expected = "No Message"
        self.assertEqual(actual, expected, "Unexpected message paramater")
    
    def test_Raises_Trash_Exception(self):
        self.assertRaises(statemanager.InvalidStateFileError, statemanager.parse_state_file, "trash_mock.yaml")
        
    def tearDown(self):
        for i in self.mock_file_dict.iterkeys():
            os.remove(i)
        
if __name__ == '__main__':
    unittest.main()
