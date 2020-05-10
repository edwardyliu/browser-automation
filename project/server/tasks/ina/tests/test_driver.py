# project/server/tasks/ina/tests/test_driver.py

# == Import(s) ==
# => Local
from project.server.tasks.ina import utils
from project.server.tasks.ina import models
from project.server.tasks.ina import driver

# => System
import os
import unittest
from pathlib import Path
from collections import deque

# == Test Object ==
class TestDriver(unittest.TestCase):
    
    def test_run(self):
        worker = driver.Driver("test_run")
        self.assertEqual(worker.key(), None)

        key = models.Key("TEST", "test_run")
        task = models.Task(key, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("printf", "Hello world, name's ${1}", ["Beau"])
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), key)
        
        response = worker.run()
        self.assertEqual(response, worker.results)
        self.assertEqual(response["${1}"], "Hello world, name's Beau")

    def test_write(self):
        worker = driver.Driver("test_write")
        key = models.Key("TEST", "test_write")
        task = models.Task(key, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("write", "//input[@name='q']", ["Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing..."]),
            models.Command("printf", "Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing...", None),
            models.Command("send_keys", None, ["${ENTER}"]),
            models.Command("pause", "2.0", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), key)

        response = worker.run({"usrId": "Edward"})
        self.assertEqual("Edward is typing..." in response["${1}"], True)

    def test_write_all(self):
        worker = driver.Driver("test_write_argv")
        key = models.Key("Test", "Writer")
        task = models.Task(key, deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("write", "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", ["${@//*[@id='video-title']}; lutv: ${@#};"]),
            models.Command("pause", "2.0", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), key)
        
        worker.run({"usrId": "Edward", "location": "Toronto"})

if __name__ == "__main__":
    unittest.main()
