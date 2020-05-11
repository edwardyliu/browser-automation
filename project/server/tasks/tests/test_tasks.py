# project/server/tasks/tests/test_api.py

# == Import(s) ==
# => Local
from project.server.tasks import tasks

# => System
import unittest

# == Test Object ==
class TestTasks(unittest.TestCase):

    def test_get_keys(self):
        names = map(lambda row: row.name, tasks.get_keys())
        self.assertEqual("TEST ALL" in names, True)
        self.assertEqual("TEST EXPECTED CONDITION" in names, True)
        self.assertEqual("TEST KEYBOARD" in names, True)
        self.assertEqual("TEST LUT" in names, True)
        self.assertEqual("TEST MOUSE" in names, True)
        self.assertEqual("TEST PRINTF" in names, True)

        self.assertEqual("FIND BY ORDER" in names, False)
        self.assertEqual("GET BY ID" in names, False)
        self.assertEqual("HOT SWAP" in names, False)

    def test_create_scan(self):
        raw = {
            "receipt": "edward.yifengliu@gmail.com",
            "data": [
                {
                    "orderId": "EdwardOrderId",
                    "lut": ""
                },
                {
                    "usrId": "Edward",
                    "name": "TEST MOUSE",
                    "lut": ""
                },
                {
                    "usrId": "Tim",
                    "name": "TEST MOUSE",
                    "lut": ""
                },
                {
                    "usrId": "Edward",
                    "name": "TEST LUT",
                    "lut": ""
                },
                {
                    "orderId": "JimOrderId",
                    "lut": ""
                }
            ]
        }
        self.assertEqual(tasks.create_scan(raw), True)

    def test_create_job(self):
        raw = {
            "receipt": "edward.yifengliu@gmail.com",
            "data": [
                {
                    "usrId": "Edward",
                    "env": "TEST",
                    "name": "TEST MOUSE",
                    "lut": ""
                },
                {
                    "usrId": "Richard",
                    "env": "TEST",
                    "name": "TEST LUT",
                    "lut": ""
                },
                {
                    "usrId": "Tim",
                    "env": "TEST",
                    "name": "TEST PRINTF",
                    "lut": ""
                },
                {
                    "usrId": "Edward",
                    "env": "TEST",
                    "name": "TEST EXPECTED CONDITION",
                    "lut": ""
                }
            ]
        }
        self.assertEqual(tasks.create_job(raw), True)

if __name__ == "__main__":
    unittest.main()
