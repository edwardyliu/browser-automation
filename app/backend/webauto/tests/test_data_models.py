# == Import(s) ==
# => Local
from .. import models
from .. import utils

# => System
import unittest
from collections import deque

class TestDataModels(unittest.TestCase):
    
    def test_model_command(self):
        command = models.Command(
            label="printf", 
            target="A beautiful mind ${1}",
            argv=["Edward"])
        self.assertEqual(command.label, "printf")
        self.assertEqual(command.target, "A beautiful mind ${1}")
        self.assertEqual(command.argv, ["Edward"])

        command.argv.append("Beau")
        self.assertEqual(command.argv, ["Edward", "Beau"])
        self.assertEqual(command.argv.pop(), "Beau")
        self.assertEqual(command.argv, ["Edward"])
    
    def test_model_key(self):
        keya = models.Key("A Test A", "DEV")
        keyb = models.Key("A Test B", "DEV")
        keyc = models.Key("A Test A", "DEV")
        lookup = {keya: "Hello Key Model A"}

        self.assertEqual(lookup[keya], "Hello Key Model A")
        self.assertEqual(lookup[keyc], "Hello Key Model A")
        self.assertEqual(keya, keyc)

        lookup[keyb] = "Hello Key Model B"
        self.assertEqual(lookup[keyb], "Hello Key Model B")

    def test_model_task(self):
        cmda = models.Command(label="printf", target="A beautiful mind ${2}", argv=["Edward", "Beau"])
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
