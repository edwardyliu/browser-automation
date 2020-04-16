# == Import(s) ==
# => Local
from . import constant
from . import utils

# => System
import time
from dataclasses import dataclass

# => External
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# == Data Model(s) ==
@dataclass(frozen=True)
class Action:
    """Define an Action:

    Execute a method/function (i.e. Action) given a keyword <key> and a list of parameters <arguments>
    """
    name: str
    key: str
    arguments: list

# == Data Class(es) ==
# => The Finite State Machine for Regular Operations
class Machine(object):

    def __init__(self, uid:str, driver:webdriver, actions:list):
        self.log = utils.get_logger(uid)
        self.driver = driver
        self.actions = actions

        self.size = len(self.actions) - 1
        self.counter = 0
    
    def next(self)->bool:
        action = self.actions[self.counter]
        getattr(self, action.key)(action.arguments)

        if self.counter < self.size:
            self.counter += 1
            return True
        else:
            self.counter = 0
            return False
    
    def click(self, argv:[str]):
        for xpath in argv:
            try:
                # locate
                elem_presence = EC.presence_of_element_located((By.XPATH, xpath))
                WebDriverWait(self.driver, constant.TIMEOUT).until(elem_presence)

                # click
                elem = self.driver.find_element_by_xpath(xpath)
                if type(elem) is list:
                    elem[0].click()
                else:
                    elem.click()

                # wait
                time.sleep(constant.CLICK)

            except exceptions.TimeoutException:
                self.log.error("machine.click: Timeout Error")
            
            except Exception:
                self.log.error("machine.click: Unknown Error")
                raise Exception

    def get(self, argv:[str]):
        try:
            # get
            url = argv[0]
            self.log.info(f"machine.get: {url}")
            self.driver.get(url)

            # wait
            time.sleep(constant.GET)
        
        except IndexError:
            self.log.error("machine.get: Index Error")
            raise IndexError
        
        except Exception:
            self.log.error("machine.get: Unknown Error")
            raise Exception
    
    def idle(self, argv:[str]=None):
        time.sleep(constant.IDLE)

    def write(self, argv:[str]):
        try:
            # extract
            xpath = argv[0]
            values = argv[1]

            # locate
            elem_presence = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.driver, constant.TIMEOUT).until(elem_presence)

            # write
            elem = self.driver.find_element_by_xpath(xpath)
            if type(elem) is list:
                elem[0].send_keys(values)
            else:
                elem.send_keys(values)
            
        except IndexError:
            self.log.error("machine.write: Index Error")
            raise IndexError
        
        except exceptions.TimeoutException:
            self.log.error("machine.write: Timeout Error")

        except Exception:
            self.log.error("machine.write: Unknown Error")
            raise Exception
    
    def wait(self, argv:[str]=None):
        try: 
            decimal = float(argv[0])
            time.sleep(decimal)

        except IndexError:
            self.idle()

        except ValueError:
            self.log.error("machine.wait: Value Error")
            raise ValueError
