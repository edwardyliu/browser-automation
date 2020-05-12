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
        self.assertEqual(instance.taskkey(), key)
        
        ilut = instance.exec({"usrId": "Edward"})
        self.assertEqual(ilut, instance.results)
        self.assertEqual(ilut["${0}"], "I am alive! Muhahahaha Edward")

    def test_printf(self):
        instance = driver.Driver("test_printf")
        key = models.Key("TEST", "test_printf")
        task = models.Task(key, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("dsend_keys", 
                "//input[@name='q']", 
                ["Wow ${usrId} is typing..."]
            ),
            models.Command("printf", "Wow ${usrId} is typing...", None),
            models.Command("send_keys", None, ["${ENTER}"]),
            models.Command("pause", "2.0", None)
        ]))
        instance.assign(task)
        self.assertEqual(instance.taskkey(), key)

        ilut = instance.exec({"usrId": "Edward"})
        self.assertEqual("Edward is typing..." in ilut["${0}"], True)

    def test_printf_all(self):
        instance = driver.Driver("test_printf_all")
        key = models.Key("Test", "test_printf_all")
        task = models.Task(key, deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("dsend_keys", 
                "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", 
                ["${@//*[@id='video-title']}; lutv - ${@#};"]
            ),
            models.Command("printf", "${@//*[@id='video-title']}; lutv - ${@#};", None),
            models.Command("pause", "2.0", None)
        ]))
        instance.assign(task)
        self.assertEqual(instance.taskkey(), key)
        
        ilut = instance.exec({"usrId": "Edward", "orderId": "###3###542"})
        self.assertEqual("lutv - usrId: Edward, orderId: ###3###542" in ilut["${0}"], True)

if __name__ == "__main__":
    unittest.main()
