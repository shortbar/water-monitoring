import unittest
import stateread

class FileHandleMock():
    def read

class TestFileFind(unittest.TestCase):
    def setUp(self):
        pass
    
    def get_file_handle_mock(self):
        
        return (1,2)
    
    def test_FileMissing(self):
        self.assertRaises(IOError, stateread.get_file_state)
        
    def test_FileNotMissing(self):
        stateread.get_file_handle = self.get_file_handle_mock
        
        actual = stateread.get_file_state()
        self.assertTupleEqual((1,2), actual, "This is a message")
        
if __name__ == '__main__':
    unittest.main()
        