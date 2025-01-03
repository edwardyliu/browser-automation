# project/server/tasks/tests/test_tasks.py

# === Import(s) ===
# => Local <=
from project.server import tasks

# => System <=
import unittest

# === Test Object ===
class TestTasks(unittest.TestCase):

    def test_get_keys(self):
        names = list( map(lambda row: row.name, tasks.keys()) )
        
        self.assertEqual("TEST ALL" in names, True)
        self.assertEqual("TEST EXPECTED CONDITION" in names, True)
        self.assertEqual("TEST KEYBOARD" in names, True)
        self.assertEqual("TEST LUT" in names, True)
        self.assertEqual("TEST MOUSE" in names, True)
        self.assertEqual("TEST PRINTF" in names, True)

        self.assertEqual("FIND ORDER" in names, False)
        self.assertEqual("GET ORDER BY ID" in names, False)
        self.assertEqual("SWAP USER" in names, False)
    
    def test_snap(self):
        raw = {
            "receipt": "edward.yifengliu@gmail.com",
            "data": [
                {
                    "usrId": "Edward",
                    "env": "DELTA",
                    "name": "GET SNAP",
                    "lut": {'url': 'https://www.bing.com/'}
                }
            ]
        }
        self.assertEqual(tasks.create_job(raw), True)

    def test_create_scan(self):
        raw = {
            "receipt": "edward.yifengliu@gmail.com",
            "data": [
                {
                    # "usrId": "Han",
                    "orderId": "HanOrderId",
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
                    # "usrId": "Steven",
                    "orderId": "StevenOrderId",
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
