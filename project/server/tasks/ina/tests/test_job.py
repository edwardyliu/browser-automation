# project/server/tasks/ina/tests/test_job.py

# == Import(s) ==
# => Local
from project.server.tasks.ina import models
from project.server.tasks.ina import job

# => System
import unittest
from collections import deque

# == Test Object ==
class TestJob(unittest.TestCase):
    
    def test_lut(self):
        key = models.Key("Test", "test_lut")
        task = models.Task(key, deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("write", 
                "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", 
                ["${@//*[@id='video-title']}; lutv - ${@#};"]
            ),
            models.Command("printf", "${@//*[@id='video-title']}; lutv - ${@#};", None),
            models.Command("pause", "2.0", None)
        ]))

        handler = job.Job()
        handler.push(task, fmt="Hello world and ${usrId}", elut={"usrId": "Edward"})
        self.assertEqual(len(handler.queue), 1)

        handler.deploy()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Hello world and Edward" in handler.lines[0], True)
        
    def test_bulk_push(self):
        key_a = models.Key("Test", "test_bulk_push")
        task_a = models.Task(key_a, deque([
            models.Command("get", "https://www.youtube.com/", None),
            models.Command("write", 
                "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input", 
                ["${@//*[@id='video-title']}; lutv - ${@#};"]
            ),
            models.Command("printf", "${@//*[@id='video-title']}; lutv - ${@#};", None),
            models.Command("pause", "2.0", None)
        ]))

        handler = job.Job()
        handler.push(task_a, elut={"usrId": "Edward"}, trace=False)
        self.assertEqual(len(handler.queue), 1)

        key_b = models.Key("TEST", "test_bulk_push")
        task_b = models.Task(key_b, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("write", 
                "//input[@name='q']", 
                ["Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing..."]
            ),
            models.Command("printf", "Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing...", None),
            models.Command("send_keys", None, ["${ENTER}"]),
            models.Command("pause", "2.0", None)
        ]))
        names = ["Edward", "John", "Suri", "Kristen", "Han", "Steven", "Will"]
        for name in names: handler.push(task_b, elut={"usrId": name})
        self.assertEqual(len(handler.queue), len(names)+1)
        
        handler.deploy()
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Edward" in handler.lines[0], True)
        self.assertEqual("John" in handler.lines[1], True)
        self.assertEqual("Suri" in handler.lines[2], True)
        self.assertEqual("Kristen" in handler.lines[3], True)
        self.assertEqual("Han" in handler.lines[4], True)
        self.assertEqual("Steven" in handler.lines[5], True)
        self.assertEqual("Will" in handler.lines[6], True)
    
    def test_email(self):
        key = models.Key("TEST", "test_email")
        task = models.Task(key, deque([
            models.Command("get", "https://www.google.com/", None),
            models.Command("write", 
                "//input[@name='q']", 
                ["Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing..."]
            ),
            models.Command("printf", "Wow ${/html/body/div/div[4]/span/center/div[3]/div[1]/div/a}! ${usrId} is typing...", None),
            models.Command("send_keys", None, ["${ENTER}"]),
            models.Command("pause", "2.0", None)
        ]))

        handler = job.Job()
        handler.push(task, elut={"usrId": "Edward Y. Liu"})
        self.assertEqual(len(handler.queue), 1)

        handler.deploy("edward.yifengliu@gmail.com")
        self.assertEqual(len(handler.queue), 0)
        self.assertEqual("Edward Y. Liu is typing..." in handler.lines[0], True)

if __name__ == "__main__":
    unittest.main()
