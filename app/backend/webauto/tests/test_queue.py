# == Import(s) ==
# => Local
from .. import models
from .. import service

# => System
import os
import unittest
from pathlib import Path

class TestQueue(unittest.TestCase):

    def test_get_keys(self):
        queue = service.Queue()
        keys = queue.get_keys()

        self.assertEqual(len(keys), 5)
        self.assertEqual(models.Key("TEST SIMPLE CURSOR STATES", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST COMPLEX CURSOR STATES", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST PRINTF", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST KEYBOARD STATES", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST GLOBAL LOOKUP TABLE", "DEV") in keys, True)
    
    def test_middleware(self):
        queue = service.Queue()
        queue.enqueue("DEV", "TEST COMPLEX CURSOR STATES", tbl={"name": "Edward", "target": "Fun"})
        queue.enqueue("DEV", "TEST COMPLEX CURSOR STATES", fmt="${1} ;; ${@}", tbl={"name": "Beau", "target": "Excitement"})
        self.assertEqual(len(queue.job_queue), 2)

        queue.submit()
        self.assertEqual(len(queue.job_queue), 0)
        self.assertEqual(len(queue.stdout), 2)
        self.assertEqual("Edward" in queue.stdout[0], True)
        self.assertEqual("Beau" in queue.stdout[1], True)
    
    def test_global_lookup_table(self):
        queue = service.Queue()
        queue.enqueue("DEV", "TEST GLOBAL LOOKUP TABLE", fmt="${1}", tbl={"username": "webauto", "noun": "world", "name": "Edward"})
        self.assertEqual(len(queue.job_queue), 1)

        queue.submit()
        self.assertEqual(len(queue.job_queue), 0)
        self.assertEqual("Hello world and Edward", queue.stdout[0])

    def test_submit_and_save(self):
        queue = service.Queue()
        queue.enqueue("DEV", "TEST COMPLEX CURSOR STATES", tbl={"name": "Edward", "target": "Fun"})

        key = "TEST PRINTF"
        fmt = "My name is ${user}! $3: ${3}."
        users = ["Edward", "John", "Suri", "Kristen", "Han", "Steven", "Will"]
        for user in users: queue.enqueue("DEV", key, fmt=fmt, tbl={"user": user})
        self.assertEqual(len(queue.job_queue), len(users)+1)

        queue.submit()
        self.assertEqual(len(queue.job_queue), 0)
        self.assertEqual("Edward" in queue.stdout[1], True)
        self.assertEqual("John" in queue.stdout[2], True)
        self.assertEqual("Suri" in queue.stdout[3], True)
        self.assertEqual("Kristen" in queue.stdout[4], True)
        self.assertEqual("Han" in queue.stdout[5], True)
        self.assertEqual("Steven" in queue.stdout[6], True)
        self.assertEqual("Will" in queue.stdout[7], True)

        queue.save(os.path.join(Path(__file__).parents[0], "testSave.csv"))

if __name__ == "__main__":
    unittest.main()
