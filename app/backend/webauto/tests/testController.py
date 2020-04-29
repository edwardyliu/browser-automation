# == Import(s) ==
# => Local
from .. import models
from .. import service

# => System
import os
import unittest
from pathlib import Path

class TestController(unittest.TestCase):

    def test_get_job_keys(self):
        controller = service.Controller()
        keys = controller.get_job_keys()

        self.assertEqual(len(keys), 4)
        self.assertEqual(models.Key("TEST SIMPLE CURSOR STATES", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST COMPLEX CURSOR STATES", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST PRINTF", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST KEYBOARD STATES", "DEV") in keys, True)
    
    def test_submit(self):
        controller = service.Controller()
        controller.enqueue("DEV", "TEST COMPLEX CURSOR STATES", argv={"name": "Edward", "target": "Fun"})
        controller.enqueue("DEV", "TEST COMPLEX CURSOR STATES", fmt="Hello World: ${1} ;; ${@}", argv={"name": "Beau", "target": "Excitement"})
        controller.submit()
        
        print(controller.stdout)
        self.assertEqual(len(controller.stdout), 2)
        self.assertEqual("Edward" in controller.stdout[0], True)
        self.assertEqual("Beau" in controller.stdout[1], True)
    
    def test_bulk_submit_and_save(self):
        controller = service.Controller()
        key = "TEST PRINTF"
        fmt = "My name is ${user}! $3: ${3}."
        users = ["Edward", "John", "Suri", "Kristen", "Han", "Steven", "Will"]
        for user in users: controller.enqueue("DEV", key, fmt=fmt, argv={"user": user})
        self.assertEqual(len(controller.job_queue), len(users))

        controller.submit()
        
        self.assertEqual(len(controller.stdout), len(users))
        self.assertEqual("Edward" in controller.stdout[0], True)
        self.assertEqual("John" in controller.stdout[1], True)
        self.assertEqual("Suri" in controller.stdout[2], True)
        self.assertEqual("Kristen" in controller.stdout[3], True)
        self.assertEqual("Han" in controller.stdout[4], True)
        self.assertEqual("Steven" in controller.stdout[5], True)
        self.assertEqual("Will" in controller.stdout[6], True)

        controller.save(os.path.join(Path(__file__).parents[0], "testSave.csv"))

if __name__ == "__main__":
    unittest.main()
