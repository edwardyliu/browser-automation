# == Import(s) ==
# => Local
from . import constant
from . import parser
from . import machine
from . import utils

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

        self.plugins = constant.PLUGINS
    
    def __enter__(self):
        self.driver.get(constant.INITIAL_PAGE)
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()

    def set_plugins(self, plugins:dict):
        self.plugins = plugins

    def make_file(self):
        print()
    
    def write(self, buf:str):
        print()

    def submit_job(self):
        print()

    def scrape_job(self):
        print()

    def scrape_uid(self):
        print()

    def alter_uid(self, uid:str):
        print("alter uid")
        time.sleep(constant.TASK)
    
    def batch_job(self, env:str, jobs:[str], uid:str):
        self.alter_uid(uid)

        for job in jobs:
            fsm = self.machines[env][job]
            while fsm.next(): pass

            time.sleep(constant.JOB)
    
    def batch_uid(self, env:str, job:str, uids:[str]):
        fsm = self.machines[env][job]

        for uid in uids:
            self.alter_uid(uid)
            while fsm.next(): pass

            time.sleep(constant.JOB)
    