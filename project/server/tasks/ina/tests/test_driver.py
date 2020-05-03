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
        worker = driver.Driver("test_simple_task")
        self.assertEqual(worker.key(), None)
        key = models.Key("Test", "Beautiful")
        task = models.Task(key, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("printf", "Hello World, me Name's ${1}", ["Beau"]),
            models.Command("pause", "5", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), key)
        
        results = worker.run()
        self.assertEqual(results, worker.results)
        self.assertEqual(results["${1}"], "Hello World, me Name's Beau")

    def test_write(self):
        worker = driver.Driver("test_write")
        key = models.Key("Test", "Writer")
        task = models.Task(key, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("write", "//input[@name='q']", ["wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}... ${name} is typing, "]),
            models.Command("send_keys", None, ["${ENTER}"]),
            models.Command("pause", "5.0", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), key)
        
        worker.run({"name": "Edward"})

    def test_write_argv(self):
        worker = driver.Driver("test_write_argv")
        key = models.Key("Test", "Writer")
        task = models.Task(key, deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("pause", "3.0", None),
            models.Command("printf", "START HERE ${//*[@id='video-title']} | name: ${name}, ${2}", ["Edward", "Beau"]),
            models.Command("write", "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", ["${//*[@id='video-title']}... ${name}"]),
            models.Command("pause", "5.0", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), key)
        
        
        worker.run({"name": "Edward", "noun": "Toronto"})

    def test_write_all(self):
        worker = driver.Driver("test_write_argv")
        key = models.Key("Test", "Writer")
        task = models.Task(key, deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("pause", "3.0", None),
            models.Command("write", "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", ["${@//*[@id='video-title']}... lutv: ${@#}... argv: ${@}"]),
            models.Command("pause", "5.0", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), key)
        
        worker.run({"name": "Edward", "noun": "Toronto"})

if __name__ == "__main__":
    unittest.main()
