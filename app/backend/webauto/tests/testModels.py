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
            target="A beautiful mind ${name}",
            argv=["Edward"])
        self.assertEqual(command.label, "printf")
        self.assertEqual(command.target, "A beautiful mind ${name}")
        self.assertEqual(command.argv, ["Edward"])

        command.argv.append("Beau")
        self.assertEqual(command.argv, ["Edward", "Beau"])
        self.assertEqual(command.argv.pop(), "Beau")
        self.assertEqual(command.argv, ["Edward"])

    def test_sequence_model(self):
        cmda = models.Command(label="printf", target="A beautiful mind ${name}", argv=["Edward"])
        cmdb = models.Command(label="printf", target="An amazing experience with ${name}", argv=["Beau"])
        cmdc = models.Command(label="printf", target="A ${name} cause", argv=["noble"])
        sequence = models.Sequence(
            name="A Web Sequence",
            env="DEV",
            cmds=deque([cmda, cmdb]))
        self.assertEqual(sequence.name, "A Web Sequence")
        self.assertEqual(sequence.env, "DEV")
        self.assertEqual(sequence.cmds, deque([cmda, cmdb]))
        
        sequence.cmds.append(cmdc)
        self.assertEqual(sequence.cmds, deque([cmda, cmdb, cmdc]))
        self.assertEqual(sequence.cmds.pop(), cmdc)
        self.assertEqual(sequence.cmds, deque([cmda, cmdb]))

    def test_worker_model(self):
        driver = utils.get_webdriver()

        worker = models.Worker("A Worker", driver)
        for sequence in utils.get_sequences():
            worker.load(sequence)
            print(f"{sequence.name}: {worker.run()}")

        driver.quit()

if __name__ == "__main__":
    unittest.main()
