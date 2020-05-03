# project/server/tasks/tests/test_service.py

# == Import(s) ==
# => Local
from project.server.tasks import service

# => System
import unittest

# == Test Object ==
class TestService(unittest.TestCase):
    
    def test_exec_job(self):
        parcel = [
            {
                "env": "TEST",
                "name": "TEST COMPLEX CURSOR STATES"
            },
            {
                "env": "TEST",
                "name": "TEST GLOBAL LOOKUP TABLE",
                "lut": {"username": "EYL", "noun": "World", "name": "Myself"}
            },
            {
                "env": "TEST",
                "name": "TEST COMPLEX CURSOR STATES"
            },
            {
                "env": "TEST",
                "name": "TEST COMPLEX CURSOR STATES"
            },
        ]
        requestor = "Edward"
        service.exec_job(parcel, requestor)

if __name__ == "__main__":
    unittest.main()
