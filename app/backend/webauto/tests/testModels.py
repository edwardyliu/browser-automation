# == Import(s) ==
# => Local
from .. import models
from .. import utils

# => System
import unittest

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
            cmds=[cmda, cmdb])
        self.assertEqual(sequence.name, "A Web Sequence")
        self.assertEqual(sequence.env, "DEV")
        self.assertEqual(sequence.cmds, [cmda, cmdb])

        sequence.cmds.append(cmdc)
        self.assertEqual(sequence.cmds, [cmda, cmdb, cmdc])
        self.assertEqual(sequence.cmds.pop(), cmdc)
        self.assertEqual(sequence.cmds, [cmda, cmdb])

    def test_worker_model(self):
        driver = utils.get_webdriver()

        sequences = utils.get_sequences()
        worker = models.Worker("A Worker", driver)
        worker.load(sequences[0])
        worker.run()

        driver.quit()

if __name__ == "__main__":
    unittest.main()
