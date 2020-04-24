# == Import(s) ==
# => Local
from .. import parser

# => System
import unittest

class TestParser(unittest.TestCase):
    
    def test_get_filepaths(self):
        result = parser.get_filepaths()
        self.assertEqual(len(result), 4)
    
    def test_get_dcgs(self):
        result = parser.get_dcgs()
        self.assertEqual(len(result), 4)

if __name__ == "__main__":
    unittest.main()
