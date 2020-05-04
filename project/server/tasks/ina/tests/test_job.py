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
        handler.push_("TEST", "TEST MOUSE", lut={"userid": "Edward"})
        handler.push_("TEST", "TEST PRINTF", lut={"else": "Beau"})
        self.assertEqual(len(handler.queue), 2)
        
        handler.exec()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Edward" in handler.lines[0], True)
        self.assertEqual("None" in handler.lines[1], True)
    
    def test_lut(self):
        handler = job.Job()
        handler.push_("TEST", "TEST LUT", fmt="Hello world and ${noun}", lut={"userid": "webauto", "noun": "Toronto"})
        self.assertEqual(len(handler.queue), 1)

        handler.exec()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Hello world and Toronto", handler.lines[0])

    def test_bulk(self):
        handler = job.Job()
        handler.push_("TEST", "TEST MOUSE", lut={"userid": "Edward"})
        self.assertEqual(len(handler.queue), 1)

        key = "TEST PRINTF"
        fmt = "My name is ${name}! $1: ${1}."
        names = ["Edward", "John", "Suri", "Kristen", "Han", "Steven", "Will"]
        for name in names: handler.push_("TEST", key, fmt=fmt, lut={"name": name})
        self.assertEqual(len(handler.queue), len(names)+1)
        
        handler.exec()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Edward" in handler.lines[1], True)
        self.assertEqual("John" in handler.lines[2], True)
        self.assertEqual("Suri" in handler.lines[3], True)
        self.assertEqual("Kristen" in handler.lines[4], True)
        self.assertEqual("Han" in handler.lines[5], True)
        self.assertEqual("Steven" in handler.lines[6], True)
        self.assertEqual("Will" in handler.lines[7], True)
    
    def test_email(self):
        handler = job.Job()

        userids = ["Edward", "Sam", "Yelp", "Beau", "Gram"]
        for userid in userids: handler.push_("TEST", "TEST LUT", lut={"userid": userid})
        self.assertEqual(len(handler.queue), len(userids))

        handler.exec("edward.yifengliu@gmail.com")
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Edward" in handler.lines[0], True)
        self.assertEqual("Sam" in handler.lines[1], True)
        self.assertEqual("Yelp" in handler.lines[2], True)
        self.assertEqual("Beau" in handler.lines[3], True)
        self.assertEqual("Gram" in handler.lines[4], True)
        
if __name__ == "__main__":
    unittest.main()
