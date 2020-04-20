# == Import(s) ==
# => Local
from . import constant
from . import parser
from . import machine

# => System
import time

# => External
from selenium import webdriver

class Controller(object):

    def __init__(self, driver:webdriver):
        self.driver = driver

        self.machines = {}
        for dcg in parser.get_dcgs():
            fsm = machine.model.Machine(dcg.name, self.driver, dcg.nodes)
            
            if dcg.env not in self.machines:
                self.machines[dcg.env] = {}
            self.machines[dcg.env][dcg.name] = fsm
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

    def alter_uid(self, uid:str):
        print("alter")
        time.sleep(constant.ALTER)

    def exec(self, env:str, jobs:[str], uid:str):
        self.alter_uid(uid)

        for job in jobs:
            fsm = self.machines[env][job]
            while fsm.next(): pass

            time.sleep(constant.JOB)
    
    def batch(self, env:str, job:str, uids:[str]):
        fsm = self.machines[env][job]

        for uid in uids:
            self.alter_uid(uid)
            while fsm.next(): pass

            time.sleep(constant.JOB)
    