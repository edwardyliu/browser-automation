# project/server/tasks/ina/tests/test_constant.py

# == Import(s) ==
# => Local
from project.server.tasks.ina import constant

# => System
import unittest

# == Test Object ==
class TestConstant(unittest.TestCase):
    
    def test_task_dict(self):
        results = constant.TASK_DICT
        self.assertEqual(len(results), 5)

    def test_task_keys(self):
        results = constant.TASK_KEYS
        self.assertEqual(len(results), 5)

if __name__ == "__main__":
    unittest.main()
