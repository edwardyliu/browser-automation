# project/server/tasks/tests/test_constant.py

# == Import(s) ==
# => Local
from project.server.tasks import ina
from project.server.tasks import constant

# => System
import unittest

# == Test Object ==
class TestConstant(unittest.TestCase):
    
    def test_task_dict(self):
        tasks = constant.TASK_DICT
        self.assertEqual(len(tasks), 6)
        self.assertEqual(ina.Key("TEST", "TEST ALL") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST EXPECTED CONDITION") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST KEYBOARD") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST LUT") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST MOUSE") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST PRINTF") in tasks, True)

    def test_task_keys(self):
        tasks = constant.TASK_KEYS
        self.assertEqual(len(tasks), 6)
        self.assertEqual(ina.Key("TEST", "TEST ALL") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST EXPECTED CONDITION") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST KEYBOARD") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST LUT") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST MOUSE") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST PRINTF") in tasks, True)
        
if __name__ == "__main__":
    unittest.main()
