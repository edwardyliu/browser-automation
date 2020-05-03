# project/server/tasks/ina/tests/test_job.py

# == Import(s) ==
# => Local
from project.server.tasks.ina import models
from project.server.tasks.ina import job

# => System
import os
import unittest
from pathlib import Path

# == Test Object ==
class TestJob(unittest.TestCase):
    
    def test_middleware(self):
        handler = job.Job()
        handler.push_("TEST", "TEST COMPLEX CURSOR STATES", lut={"name": "Edward", "target": "Fun"})
        handler.push_("TEST", "TEST COMPLEX CURSOR STATES", fmt="${@#}", lut={"name": "Beau", "target": "Excitement"})
        self.assertEqual(len(handler.queue), 2)
        
        handler.exec()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Edward" in handler.results[0], True)
        self.assertEqual("Beau" in handler.results[1], True)
    
    def test_lookup_table(self):
        handler = job.Job()
        handler.push_("TEST", "TEST GLOBAL LOOKUP TABLE", fmt="Hello world and ${name}", lut={"username": "webauto", "noun": "world", "name": "Edward"})
        self.assertEqual(len(handler.queue), 1)

        handler.exec()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Hello world and Edward", handler.results[0])

    def test_task_reassign(self):
        handler = job.Job()
        handler.push_("TEST", "TEST COMPLEX CURSOR STATES", lut={"name": "Edward", "target": "Fun"})

        key = "TEST PRINTF"
        fmt = "My name is ${user}! $2: ${2}."
        users = ["Edward", "John", "Suri", "Kristen", "Han", "Steven", "Will"]
        for user in users: handler.push_("TEST", key, fmt=fmt, lut={"user": user})
        self.assertEqual(len(handler.queue), len(users)+1)
        
        handler.exec()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Edward" in handler.results[1], True)
        self.assertEqual("John" in handler.results[2], True)
        self.assertEqual("Suri" in handler.results[3], True)
        self.assertEqual("Kristen" in handler.results[4], True)
        self.assertEqual("Han" in handler.results[5], True)
        self.assertEqual("Steven" in handler.results[6], True)
        self.assertEqual("Will" in handler.results[7], True)

if __name__ == "__main__":
    unittest.main()
