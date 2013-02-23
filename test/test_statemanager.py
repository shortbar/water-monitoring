# test_stateread.py
# Patrick Souza <souza.patrick@gmail.com> for Prefiat LLC
# Test methods for the statread.py method: reading system state.

import unittest
import stateread
import yaml
import os
import datetime
import states

class TestFileFind(unittest.TestCase):
    def setUp(self):
        
        #Create mock files for testing
        self.mock_file_dict = {"empty_mock.yaml" : "",
                               "normal_mock.yaml" :    """---\n
                                                       state : okay\n
                                                       since_local : !!timestamp '2013-02-10 13:12:11'\n
                                                       message : No Message""",
                               "warning_mock.yaml":    """---\n
                                                      state : warning\n
                                                      since_local : !!timestamp '2013-02-15 13:12:11'\n
                                                      message : No Message""",
                               "action_mock.yaml":    """---\n
                                                      state : action\n
                                                      since_local : !!timestamp '2013-02-28 13:12:11'\n
                                                      message : No Message""",
                                "trash_mock.yaml":   """a;slkdfj;laskjdf;akj""",
                                
                                }
        for i in self.mock_file_dict.iterkeys():
            f = open(i, "w+")
            f.write(self.mock_file_dict[i])
            f.close                
                    
    def test_FileMissing(self):
        self.assertRaises(stateread.MissingStateFileError, stateread.get_file_handle, "nonexistent.yaml")
        
    def test_FileNotMissing(self):  
        actual = stateread.get_file_handle("empty_mock.yaml")
        self.assertIs(type(actual), file, "File is missing")
        
    def test_Recovers_OK_State(self):
        actual = stateread.parse_state_file("normal_mock.yaml")
        self.assertIsInstance(actual, states.OKState, "Error Recovering OK State")
        
    def test_Recovers_Warning_State(self):
        actual = stateread.parse_state_file("warning_mock.yaml")
        self.assertIsInstance(actual, states.WarningState, "Error Recovering Warning State")
    
    def test_Recovers_Alert_State(self):
        actual = stateread.parse_state_file("action_mock.yaml")
        self.assertIsInstance(actual, states.ActionState, "Error Recovering Action State")
    
    def test_Recovers_correct_date(self):
        actual = stateread.parse_state_file("normal_mock.yaml").since
        expected = datetime.datetime(2013, 2, 10, 13, 12, 11)
        self.assertEqual(actual, expected, "Unexpected datetime")
    
    def test_Recovers_correct_message(self):
        actual = stateread.parse_state_file("normal_mock.yaml").message
        expected = "No Message"
        self.assertEqual(actual, expected, "Unexpected message paramater")
    
    def test_Raises_Trash_Exception(self):
        self.assertRaises(stateread.InvalidStateFileError, stateread.parse_state_file, "trash_mock.yaml")
        
    def tearDown(self):
        for i in self.mock_file_dict.iterkeys():
            os.remove(i)
        
if __name__ == '__main__':
    unittest.main()
