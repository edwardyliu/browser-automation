# == Import(s) ==
# => Local
from .. import utils

# => System
import unittest

class TestUtils(unittest.TestCase):
    
    def test_get_sequences(self):
        results = utils.get_sequences()
        self.assertEqual(len(results), 2)
    
        log = utils.get_logger("test_get_sequences")
        results = utils.get_sequences(log=log)
        self.assertEqual(len(results), 2)

if __name__ == "__main__":
    unittest.main()
