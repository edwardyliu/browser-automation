# == Import(s) ==
# => Local
from . import constant

# => System
import time

# => External


class Machine(object):
    def __init__(self, id:str):
        self.id = id
    
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
    