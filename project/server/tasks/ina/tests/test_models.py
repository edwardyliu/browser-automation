# project/server/tasks/ina/tests/test_models.py

# == Import(s) ==
# => Local
from project.server.tasks.ina import utils
from project.server.tasks.ina import models

# => System
import unittest
from collections import deque

# == Test Object ==
class TestModels(unittest.TestCase):
    
    def test_command(self):
        command = models.Command(label="printf", target="A beautiful mind ${1}", argv=["Edward"])
        self.assertEqual(command.label, "printf")
        self.assertEqual(command.target, "A beautiful mind ${1}")
        self.assertEqual("Edward" in command.argv, True)

        command.argv.append("Beau")
        self.assertEqual(command.argv, ["Edward", "Beau"])
        self.assertEqual(command.argv.pop(), "Beau")
        self.assertEqual(command.argv, ["Edward"])
    
    def test_key(self):
        keya = models.Key("TEST", "Test A")
        keyb = models.Key("TEST", "Test B")
        keyc = models.Key("TEST", "Test A")
        self.assertEqual(keya, keyc)

        lookup = {keya: "Hello Key A"}
        self.assertEqual(lookup[keya], "Hello Key A")
        self.assertEqual(lookup[keyc], "Hello Key A")
        
        lookup[keyb] = "Hello Key Model B"
        self.assertEqual(lookup[keyb], "Hello Key Model B")

    def test_task(self):
        cmda = models.Command(label="printf", target="A beautiful mind ${2}", argv=["Beau", "Edward"])
        cmdb = models.Command(label="printf", target="An amazing experience with ${1}", argv=["Jim"])
        cmdc = models.Command(label="printf", target="A ${1} cause", argv=["noble"])
        key = models.Key("DEV", "A Web Task")
        task = models.Task(key=key, cmds=deque([cmda, cmdb]))
        self.assertEqual(task.key, key)
        self.assertEqual(task.cmds, deque([cmda, cmdb]))
        
        task.cmds.append(cmdc)
        self.assertEqual(task.cmds, deque([cmda, cmdb, cmdc]))
        self.assertEqual(task.cmds.pop(), cmdc)
        self.assertEqual(task.cmds, deque([cmda, cmdb]))
        
if __name__ == "__main__":
    unittest.main()
