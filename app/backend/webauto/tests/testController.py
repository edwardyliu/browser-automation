# == Import(s) ==
# => Local
from .. import services

# => System
import os
import unittest
from pathlib import Path

class TestController(unittest.TestCase):

    def test_get_job_keys(self):
        controller = services.Controller()
        keys = controller.get_job_keys()

        self.assertEqual(len(keys), 4)
        self.assertEqual("TEST SIMPLE CURSOR STATES" in keys, True)
        self.assertEqual("TEST COMPLEX CURSOR STATES" in keys, True)
        self.assertEqual("TEST PRINTF" in keys, True)
        self.assertEqual("TEST KEYBOARD STATES" in keys, True)
    
    def test_submit(self):
        controller = services.Controller()
        controller.enqueue("TEST COMPLEX CURSOR STATES", argv={"name": "Edward", "target": "Fun"})
        controller.enqueue("TEST COMPLEX CURSOR STATES", fmt="Hello World: ${@}", argv={"name": "Beau", "target": "Excitement"})
        controller.submit()

        self.assertEqual(len(controller.stdout), 2)
        self.assertEqual("Edward" in controller.stdout[0], True)
        self.assertEqual("Beau" in controller.stdout[1], True)
    
    def test_bulk_submit_and_save(self):
        controller = services.Controller()
        key = "TEST PRINTF"
        fmt = "My name is ${user}! $2: ${2}."
        users = ["Edward", "John", "Suri", "Kristen", "Han", "Steven", "Will"]
        for user in users: controller.enqueue(key, fmt=fmt, argv={"user": user})
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
