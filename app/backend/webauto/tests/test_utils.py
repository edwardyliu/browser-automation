# == Import(s) ==
# => Local
from .. import utils

# => System
import unittest

class TestUtils(unittest.TestCase):
    
    def test_get_sequences(self):
        results = utils.get_tasks()
        self.assertEqual(len(results), 5)
    
        log = utils.get_logger("test_get_tasks")
        results = utils.get_tasks(log=log)
        self.assertEqual(len(results), 5)

if __name__ == "__main__":
    unittest.main()
