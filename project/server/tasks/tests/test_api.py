# project/server/tasks/tests/test_api.py

# == Import(s) ==
# => Local
from project.server.tasks import api

# => System
import unittest

# == Test Object ==
class TestAPI(unittest.TestCase):
    
    def test_create_task(self):
        message = {
            "receiver": "edward.yifengliu@gmail.com",
            "parcel": [
                {
                    "env": "TEST",
                    "name": "TEST MOUSE",
                    "lut": {"userid": "Edward"}
                },
                {
                    "env": "TEST",
                    "name": "TEST LUT",
                    "lut": {"userid": "Kim"}
                },
                {
                    "env": "TEST",
                    "name": "TEST MOUSE",
                    "lut": {"userid": "Tim"}
                },
                {
                    "env": "TEST",
                    "name": "TEST MOUSE",
                    "lut": {"userid": "Bim"}
                }
            ]
        }
        api.create_task(message)

if __name__ == "__main__":
    unittest.main()
