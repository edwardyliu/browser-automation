# project/server/tasks/tests/__main__.py

# == Import(s) ==
# => System
import unittest

# == Module Test: Tasks ==
def tests()->bool:
    tests = unittest.TestLoader().discover("project/server/tasks/", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful(): return 0
    else: return 1

if __name__ == "__main__":
    tests()
