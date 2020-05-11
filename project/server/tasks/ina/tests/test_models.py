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
        command = models.Command(label="dsend_keys", target="AN_XPATH_VALUE", argv=["Edward", "John"])
        self.assertEqual(command.label, "dsend_keys")
        self.assertEqual(command.target, "AN_XPATH_VALUE")
        self.assertEqual("Edward" in command.argv, True)

        command.argv.append("Beau")
        self.assertEqual(command.argv, ["Edward", "John", "Beau"])
        self.assertEqual(command.argv.pop(), "Beau")
        self.assertEqual(command.argv, ["Edward", "John"])
    
    def test_key(self):
        key_a = models.Key("TEST", "TestA")
        key_b = models.Key("TEST", "TestB")
        key_c = models.Key("TEST", "TestA")
        self.assertEqual(key_a, key_c)

        lut = {key_a: "Hello KeyA"}
        self.assertEqual(lut[key_a], "Hello KeyA")
        self.assertEqual(lut[key_c], "Hello KeyA")
        
        lut[key_b] = "Hello KeyB"
        self.assertEqual(lut[key_b], "Hello KeyB")

    def test_task(self):
        cmd_a = models.Command(label="dsend_keys", target="AN_XPATH_VALUE", argv=["Beau", "Edward"])
        cmd_b = models.Command(label="dsend_keys", target="AN_XPATH_VALUE", argv=["Jim"])
        cmd_c = models.Command(label="dsend_keys", target="AN_XPATH_VALUE", argv=["Noble"])
        key = models.Key("TEST", "SomeKey")
        task = models.Task(key=key, cmds=deque([cmd_a, cmd_b]))
        self.assertEqual(task.key, key)
        self.assertEqual(task.cmds, deque([cmd_a, cmd_b]))
        
        task.cmds.append(cmd_c)
        self.assertEqual(task.cmds, deque([cmd_a, cmd_b, cmd_c]))
        self.assertEqual(task.cmds.pop(), cmd_c)
        self.assertEqual(task.cmds, deque([cmd_a, cmd_b]))
        
if __name__ == "__main__":
    unittest.main()
