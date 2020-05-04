# project/server/tasks/ina/tests/test_utils.py

# == Import(s) ==
# => Local
from project.server.tasks.ina import utils
from project.server.tasks.ina import models

# => System
import unittest

# == Test Object ==
class TestUtils(unittest.TestCase):
    
    def test_get_tasklist(self):
        tasks = utils.get_tasklist()
        task_keys = list(map(lambda task: task.key, tasks))
        self.assertEqual(len(tasks), 6)
        self.assertEqual(models.Key("TEST", "TEST ALL") in task_keys, True)
        self.assertEqual(models.Key("TEST", "TEST EXPECTED CONDITION") in task_keys, True)
        self.assertEqual(models.Key("TEST", "TEST KEYBOARD") in task_keys, True)
        self.assertEqual(models.Key("TEST", "TEST LUT") in task_keys, True)
        self.assertEqual(models.Key("TEST", "TEST MOUSE") in task_keys, True)
        self.assertEqual(models.Key("TEST", "TEST PRINTF") in task_keys, True)

    def test_get_taskdict(self):
        tasks = utils.get_taskdict()
        self.assertEqual(len(tasks), 6)
        self.assertEqual(models.Key("TEST", "TEST ALL") in tasks, True)
        self.assertEqual(models.Key("TEST", "TEST EXPECTED CONDITION") in tasks, True)
        self.assertEqual(models.Key("TEST", "TEST KEYBOARD") in tasks, True)
        self.assertEqual(models.Key("TEST", "TEST LUT") in tasks, True)
        self.assertEqual(models.Key("TEST", "TEST MOUSE") in tasks, True)
        self.assertEqual(models.Key("TEST", "TEST PRINTF") in tasks, True)

if __name__ == "__main__":
    unittest.main()
