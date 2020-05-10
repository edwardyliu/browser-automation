# project/server/tasks/ina/tests/test_job.py

# == Import(s) ==
# => Local
from project.server.tasks.ina import models
from project.server.tasks.ina import job

# => System
import os
import unittest
from pathlib import Path
from collections import deque

# == Test Object ==
class TestJob(unittest.TestCase):
    
    def test_lut(self):
        key = models.Key("Test", "Writer")
        task = models.Task(key, deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("write", "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", ["${@//*[@id='video-title']}; lutv: ${@#};"]),
            models.Command("printf", "Hello World", None),
            models.Command("pause", "2.0", None)
        ]))

        handler = job.Job()
        handler.push(task, fmt="Hello world and ${noun}", lut={"usrId": "webauto", "location": "Toronto"})
        self.assertEqual(len(handler.queue), 1)

        handler.exec()
        self.assertEqual(len(handler.queue), 0)

    def test_bulk(self):
        keya = models.Key("Test", "Writer")
        taska = models.Task(keya, deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("write", "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", ["${@//*[@id='video-title']}; lutv: ${@#};"]),
            models.Command("printf", "Hello World", None),
            models.Command("pause", "2.0", None)
        ]))

        handler = job.Job()
        handler.push(taska, lut={"usrId": "Edward"})
        self.assertEqual(len(handler.queue), 1)

        keyb = models.Key("TEST", "test_write")
        taskb = models.Task(keyb, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("write", "//input[@name='q']", ["Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing..."]),
            models.Command("printf", "Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing...", None),
            models.Command("send_keys", None, ["${ENTER}"]),
            models.Command("pause", "2.0", None)
        ]))
        names = ["Edward", "John", "Suri", "Kristen", "Han", "Steven", "Will"]
        for name in names: handler.push(taskb, lut={"usrId": name})
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
        key = models.Key("TEST", "test_write")
        task = models.Task(key, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("write", "//input[@name='q']", ["Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing..."]),
            models.Command("printf", "Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing...", None),
            models.Command("send_keys", None, ["${ENTER}"]),
            models.Command("pause", "2.0", None)
        ]))

        handler = job.Job()
        handler.push(task, lut={"usrId": "Edward Y. Liu"})
        self.assertEqual(len(handler.queue), 1)

        handler.exec("edward.yifengliu@gmail.com")
        self.assertEqual(len(handler.queue), 0)
        
if __name__ == "__main__":
    unittest.main()
