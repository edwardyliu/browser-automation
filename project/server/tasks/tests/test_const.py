# project/server/tasks/tests/test_const.py

# === Import(s) ===
# => Local <=
from project.server.tasks import ina
from project.server.tasks import const

# => System <=
import unittest

# === Test Object ===
class TestConst(unittest.TestCase):
    
    def test_taskdict(self):
        tasks = const.TASKDICT

        self.assertEqual(ina.Key("TEST", "TEST ALL") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST EXPECTED CONDITION") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST KEYBOARD") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST LUT") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST MOUSE") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST PRINTF") in tasks, True)

    def test_taskkeys(self):
        tasks = const.TASKKEYS

        self.assertEqual(ina.Key("TEST", "TEST ALL") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST EXPECTED CONDITION") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST KEYBOARD") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST LUT") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST MOUSE") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST PRINTF") in tasks, True)
    
    def test_tasks(self):
        self.assertEqual(ina.Key("STATE CHANGE", "FIND BY ORDER"), const.TASK_FINDBYORDER.key)
        self.assertEqual(ina.Key("STATE CHANGE", "GET BY ID"), const.TASK_GETBYID.key)
        self.assertEqual(ina.Key("STATE CHANGE", "HOT SWAP"), const.TASK_HOTSWAP.key)

if __name__ == "__main__":
    unittest.main()
