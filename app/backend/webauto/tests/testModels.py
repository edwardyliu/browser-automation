# == Import(s) ==
# => Local
from .. import models
from .. import utils

# => System
import unittest
from collections import deque

class TestModels(unittest.TestCase):
    
    def test_command_model(self):
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
    
    def test_key_model(self):
        keya = models.Key("A Test A", "DEV")
        keyb = models.Key("A Test B", "DEV")
        keyc = models.Key("A Test A", "DEV")
        lookup = {keya: "Hello Key Model A"}

        self.assertEqual(lookup[keya], "Hello Key Model A")
        self.assertEqual(lookup[keyc], "Hello Key Model A")
        self.assertEqual(keya, keyc)

        lookup[keyb] = "Hello Key Model B"
        self.assertEqual(lookup[keyb], "Hello Key Model B")

    def test_sequence_model(self):
        cmda = models.Command(label="printf", target="A beautiful mind ${1}", argv=["Edward"])
        cmdb = models.Command(label="printf", target="An amazing experience with ${1}", argv=["Beau"])
        cmdc = models.Command(label="printf", target="A ${1} cause", argv=["noble"])
        key = models.Key("A Web Sequence", "DEV")
        sequence = models.Sequence(key=key, cmds=deque([cmda, cmdb]))
        self.assertEqual(sequence.key, key)
        self.assertEqual(sequence.cmds, deque([cmda, cmdb]))
        
        sequence.cmds.append(cmdc)
        self.assertEqual(sequence.cmds, deque([cmda, cmdb, cmdc]))
        self.assertEqual(sequence.cmds.pop(), cmdc)
        self.assertEqual(sequence.cmds, deque([cmda, cmdb]))

    def test_worker_model(self):
        driver = utils.get_webdriver()

        worker = models.Worker("A Worker", driver)
        sequence = utils.get_sequences()[0]
        worker.load(sequence)
        print(f"{sequence.key}: {worker.run()}")
        
        driver.quit()

if __name__ == "__main__":
    unittest.main()
