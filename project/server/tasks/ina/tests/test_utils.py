# project/server/tasks/ina/tests/test_utils.py

# == Import(s) ==
# => Local
from project.server.tasks.ina import utils

# => System
import unittest

# == Test Object ==
class TestUtils(unittest.TestCase):
    
    def test_get_tasklist(self):
        results = utils.get_tasklist()
        self.assertEqual(len(results), 5)

    def test_get_taskdict(self):
        results = utils.get_taskdict()
        self.assertEqual(len(results), 5)

if __name__ == "__main__":
    unittest.main()
