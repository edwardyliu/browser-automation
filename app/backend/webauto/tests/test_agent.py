# == Import(s) ==
# => Local
from .. import models
from .. import agent

# => System
import os
import unittest
from pathlib import Path

class TestAgent(unittest.TestCase):

    def test_get_keys(self):
        handler = agent.Agent()
        keys = handler.get_keys()

        self.assertEqual(len(keys), 5)
        self.assertEqual(models.Key("TEST SIMPLE CURSOR STATES", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST COMPLEX CURSOR STATES", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST PRINTF", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST KEYBOARD STATES", "DEV") in keys, True)
        self.assertEqual(models.Key("TEST GLOBAL LOOKUP TABLE", "DEV") in keys, True)
    
    def test_middleware(self):
        handler = agent.Agent()
        handler.push("DEV", "TEST COMPLEX CURSOR STATES", tbl={"name": "Edward", "target": "Fun"})
        handler.push("DEV", "TEST COMPLEX CURSOR STATES", fmt="${1} ;; ${@}", tbl={"name": "Beau", "target": "Excitement"})
        self.assertEqual(len(handler.queue), 2)

        handler.exec()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual(len(handler.results), 2)
        self.assertEqual("Edward" in handler.results[0], True)
        self.assertEqual("Beau" in handler.results[1], True)
    
    def test_global_lookup_table(self):
        handler = agent.Agent()
        handler.push("DEV", "TEST GLOBAL LOOKUP TABLE", fmt="${1}", tbl={"username": "webauto", "noun": "world", "name": "Edward"})
        self.assertEqual(len(handler.queue), 1)

        handler.exec()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Hello world and Edward", handler.results[0])

    def test_submit_and_save(self):
        handler = agent.Agent()
        handler.push("DEV", "TEST COMPLEX CURSOR STATES", tbl={"name": "Edward", "target": "Fun"})

        key = "TEST PRINTF"
        fmt = "My name is ${user}! $3: ${3}."
        users = ["Edward", "John", "Suri", "Kristen", "Han", "Steven", "Will"]
        for user in users: handler.push("DEV", key, fmt=fmt, tbl={"user": user})
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
