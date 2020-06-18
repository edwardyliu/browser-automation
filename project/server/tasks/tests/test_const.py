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
        tasks = const.TASKS_DICT

        self.assertEqual(ina.Key("TEST", "TEST ALL") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST EXPECTED CONDITION") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST KEYBOARD") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST LUT") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST MOUSE") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST PRINTF") in tasks, True)

    def test_taskkeys(self):
        tasks = const.TASKS_KEYS

        self.assertEqual(ina.Key("TEST", "TEST ALL") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST EXPECTED CONDITION") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST KEYBOARD") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST LUT") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST MOUSE") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST PRINTF") in tasks, True)
    
    def test_tasks(self):
        self.assertEqual(ina.Key("DELTA", "FIND ORDER"), const.TASK_FIND_ORDER.key)
        self.assertEqual(ina.Key("DELTA", "GET ORDER BY ID"), const.TASK_GET_ORDER_BY_ID.key)
        self.assertEqual(ina.Key("DELTA", "SWAP USER"), const.TASK_SWAP_USER.key)
        self.assertEqual(ina.Key("DELTA", "GET SNAP"), const.TASK_GET_SNAP.key)

if __name__ == "__main__":
    unittest.main()
