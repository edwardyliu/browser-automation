# == Import(s) ==
# => Local
from . import constant
from . import model
from . import utils

# => System
import time

# => External

# == Class: The Finite State Machine ==
class Machine(object):
    def __init__(self, uid:str, methods:[model.Method]):
        self.log = utils.get_logger(uid)
        self.methods = methods

        self.size = len(self.methods) - 1
        self.counter = 0
    
    def next(self)->bool:
        print("to next state")

        if self.counter == self.size:
            self.counter = 0
            return True
        else:
            self.counter += 1
            return False
    
    def idle(self, argv:[str]=None):
        time.sleep(constant.IDLE)
    
    def open(self, argv:[str]=None):
        print("spin up new state machine")
    
    def close(self, argv:[str]=None):
        print("close current state machine")
    
    def get(self, argv:[str]):
        url = argv[0]
        print(f"get url {url}")
    
    def click(self, argv:[str]):
        for xpath in argv:
            elem = xpath
            print(f"click elem {elem}")

            time.sleep(constant.CLICK)
    
    def write(self, argv:[str]):
        xpath = argv[0]
        txt = argv[1]

        elem = xpath
        print(f"write {txt} to elem {elem}")
    
    def wait(self, argv:[str]=None):
        try: 
            decimal = float(argv[0])
            time.sleep(decimal)
        except Exception:
            self.idle(argv)
    