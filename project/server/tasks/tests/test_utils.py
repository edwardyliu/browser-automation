# project/server/tasks/tests/test_utils.py

# === Import(s) ===
# => Local <=
from project.server.tasks import ina
from project.server.tasks import utils

# => System <=
import unittest

# === Test Object ===
class TestUtils(unittest.TestCase):
    
    def test_get_tasklist(self):
        tasks = utils.get_tasklist()
        task_keys = list(map(lambda task: task.key, tasks))

        self.assertEqual(ina.Key("TEST", "TEST ALL") in task_keys, True)
        self.assertEqual(ina.Key("TEST", "TEST EXPECTED CONDITION") in task_keys, True)
        self.assertEqual(ina.Key("TEST", "TEST KEYBOARD") in task_keys, True)
        self.assertEqual(ina.Key("TEST", "TEST LUT") in task_keys, True)
        self.assertEqual(ina.Key("TEST", "TEST MOUSE") in task_keys, True)
        self.assertEqual(ina.Key("TEST", "TEST PRINTF") in task_keys, True)

    def test_get_taskdict(self):
        tasks = utils.get_taskdict()

        self.assertEqual(ina.Key("TEST", "TEST ALL") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST EXPECTED CONDITION") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST KEYBOARD") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST LUT") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST MOUSE") in tasks, True)
        self.assertEqual(ina.Key("TEST", "TEST PRINTF") in tasks, True)

    def test_partition(self):
        odds, evens = utils.partition(lambda row: row % 2, range(10))

        self.assertEqual(list(odds), [1, 3, 5, 7, 9])
        self.assertEqual(list(evens), [0, 2, 4, 6, 8])

if __name__ == "__main__":
    unittest.main()
