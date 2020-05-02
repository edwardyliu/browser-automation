# == Import(s) ==
# => Local
from .. import utils
from .. import models

# => System
import os
import unittest
from pathlib import Path
from collections import deque

class TestWorker(unittest.TestCase):

    def test_simple_task(self):
        worker = models.Worker("test_simple_task")
        self.assertEqual(worker.key(), None)

        task = models.Task("Beautiful", deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("printf", "Hello World, me Name's ${1}", ["Beau"]),
            models.Command("pause", "5", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), "Beautiful")
        
        results = worker.run()
        self.assertEqual(results, worker.results)
        self.assertEqual(results["${1}"], "Hello World, me Name's Beau")

    def test_write(self):
        worker = models.Worker("test_write")
        task = models.Task("Writer", deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("write", "//input[@name='q']", ["wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}... ${name} is typing, "]),
            models.Command("send_keys", None, ["${ENTER}"]),
            models.Command("pause", "5.0", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), "Writer")
        
        worker.run({"name": "Edward"})

    def test_write_argv(self):
        worker = models.Worker("test_write_argv")
        task = models.Task("Writer", deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("pause", "3.0", None),
            models.Command("printf", "START HERE ${//*[@id='video-title']} | name: ${name}, ${2}", ["Edward", "Beau"]),
            models.Command("write", "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", ["${//*[@id='video-title']}... ${name}"]),
            models.Command("pause", "5.0", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), "Writer")
        
        
        worker.run({"name": "Edward", "noun": "Toronto"})
        print(worker.results["${1}"])

    def test_write_all(self):
        worker = models.Worker("test_write_argv")
        task = models.Task("Writer", deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("pause", "3.0", None),
            models.Command("write", "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", ["${@//*[@id='video-title']}... tblv: ${@#}... argv: ${@}"]),
            models.Command("pause", "5.0", None)
        ]))
        worker.assign(task)
        self.assertEqual(worker.key(), "Writer")
        
        worker.run({"name": "Edward", "noun": "Toronto"})

if __name__ == "__main__":
    unittest.main()
