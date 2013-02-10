import unittest
import stateread
import yaml
import os
import datetime


class TestFileFind(unittest.TestCase):
    def setUp(self):
        
        #Create mock files for testing
        self.mock_file_dict = {"empty_mock.yaml" : "",
                               "normal_mock.yaml" :    """---\n
                                                       State : Okay\n
                                                       Timestamp : !!timestamp '2013-02-10 13:12:11'\n
                                                       Message : No Message"""
                               }
        for i in self.mock_file_dict.iterkeys():
            f = open(i, "w+")
            f.write(self.mock_file_dict[i])
            f.close                
        
    
    def test_FileMissing(self):
        self.assertRaises(IOError, lambda: stateread.get_file_handle("nonexistent.yaml"))
        
    def test_FileNotMissing(self):  
        actual = stateread.get_file_handle("empty_mock.yaml")
        self.assertIs(type(actual), file, "File is missing")
    
    def test_Parse_Parameters(self):
        actual_state = stateread.parse_state_file("normal_mock.yaml")
        for i in actual_state.iterkeys():
            self.assertIn(i, ["State", "Timestamp", "Message"], "Invalid State Keys")
        self.assertIn(actual_state["State"], ["Okay","Warning","Alert"], "Error reading system state")
        self.assertIs(type(actual_state["Timestamp"]), datetime.datetime, "Error reading datetime")
        self.assertIs(type(actual_state["Message"]), str, "Error reading string")
    
    def tearDown(self):
        for i in self.mock_file_dict.iterkeys():
            os.remove(i)
        
            
        
        
if __name__ == '__main__':
    unittest.main()
        