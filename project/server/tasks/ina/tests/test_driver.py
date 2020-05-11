# project/server/tasks/ina/tests/test_driver.py

# == Import(s) ==
# => Local
from project.server.tasks.ina import models
from project.server.tasks.ina import driver

# => System
import unittest
from collections import deque

# == Test Object ==
class TestDriver(unittest.TestCase):
    
    def test_run(self):
        instance = driver.Driver("test_run")
        self.assertEqual(instance.taskkey(), None)

        key = models.Key("TEST", "test_run")
        task = models.Task(key, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("printf", "I am alive! Muhahahaha ${usrId}", None)
        ]))
        instance.assign(task)
        self.assertEqual(instance.key(), key)
        
        ilut = instance.exec({"usrId": "Edward"})
        self.assertEqual(ilut, instance.results)
        self.assertEqual(ilut["${0}"], "I am alive! Muhahahaha Edward")

    def test_write(self):
        instance = driver.Driver("test_write")
        key = models.Key("TEST", "test_write")
        task = models.Task(key, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("write", "//input[@name='q']", ["Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing..."]),
            models.Command("printf", "Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing...", None),
            models.Command("send_keys", None, ["${ENTER}"]),
            models.Command("pause", "2.0", None)
        ]))
        instance.assign(task)
        self.assertEqual(instance.key(), key)

        ilut = instance.run({"usrId": "Edward"})
        self.assertEqual("Edward is typing..." in ilut["${0}"], True)

    def test_write_all(self):
        instance = driver.Driver("test_write_all")
        key = models.Key("Test", "test_write_all")
        task = models.Task(key, deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("write", 
                "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", 
                ["${@//*[@id='video-title']}; lutv - ${@#};"]
            ),
            models.Command("printf", "${@//*[@id='video-title']}; lutv - ${@#};"),
            models.Command("pause", "2.0", None)
        ]))
        instance.assign(task)
        self.assertEqual(instance.key(), key)
        
        ilut = instance.run({"usrId": "Edward", "orderId": "###3###542"})
        self.assertEqual("lutv - usrId: Edward, orderId: ###3###542" in ilut["${0}"], True)

if __name__ == "__main__":
    unittest.main()
