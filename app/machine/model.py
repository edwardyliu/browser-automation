# == Import(s) ==
# => Local
from . import constant
from . import utils

# => System
import os
import time
from collections import deque
from dataclasses import dataclass

# => External
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
class Machine(object):
    """A Finite State Machine generated via the JSON input files

    """

    def __init__(self, uid:str, driver:webdriver, actions:list, filepath:str=None):
        self.log = utils.get_logger(uid)
        self.driver = driver
        self.actions = actions

        self.size = len(self.actions) - 1
        self.counter = 0
    
    def next(self)->bool:
        """The transition function
        Perform the action and proceed to the next state

        """
        action = self.actions[self.counter]
        getattr(self, action.key)(action.arguments)

        if self.counter < self.size:
            self.counter += 1
            return True
        else:
            self.counter = 0
            return False
    
    def idle(self, argv:[str]=None):
        """An action state - idle
        Idle (i.e. sleep) for constant.IDLE second(s)

        """
        time.sleep(constant.IDLE)

    def wait(self, argv:[str]=None):
        """An action state - wait
        Wait <decimal> seconds

        Parameters
        ----------
        argv: [str], optional
            A float, which contains the decimal value
        """
        try: 
            decimal = float(argv[0])
            time.sleep(decimal)

        except IndexError:
            self.idle()

        except ValueError:
            self.log.error("machine.wait: Value Error")
            raise ValueError

    def to(self, argv:[str]):
        """An action state - to
        To <url> page

        Parameters
        ----------
        argv: [str]
            A string, which contains the url value
        """
        try:
            # to i.e. get url
            url = argv[0]
            self.log.info(f"machine.to: {url}")
            self.driver.get(url)

            # wait
            time.sleep(constant.TO)
        
        except IndexError:
            self.log.error("machine.to: Index Error")
            raise IndexError
        
        except Exception:
            self.log.error("machine.to: Unknown Error")
            raise Exception

    def click(self, argv:[str]):
        """An action state - click
        Click the <xpath> element

        Parameters
        ----------
        argv: [str]
            A list of strings, which contains the xpath value(s)
        """
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

    def double_click(self, argv:[str]):
        """An action state - double_click
        Double-click the <xpath> element

        Parameters
        ----------
        argv: [str]
            A list of strings, which contains the xpath value(s)
        """
        for xpath in argv:
            try:
                # locate
                elem_presence = EC.presence_of_element_located((By.XPATH, xpath))
                WebDriverWait(self.driver, constant.TIMEOUT).until(elem_presence)

                # double-click
                elem = self.driver.find_element_by_xpath(xpath)
                if type(elem) is list:
                    elem[0].double_click()
                else:
                    elem.double_click()

                # wait
                time.sleep(constant.DOUBLE_CLICK)

            except exceptions.TimeoutException:
                self.log.error("machine.double_click: Timeout Error")
            
            except Exception:
                self.log.error("machine.double_click: Unknown Error")
                raise Exception

    def send_keys(self, argv:[str]):
        """An action state - send_keys
        Send-keys <values> to the <xpath> element

        Parameters
        ----------
        argv: [str]
            A tuple2, which contains the xpath value and 'values' value
        """
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
            self.log.error("machine.send_keys: Index Error")
            raise IndexError
        
        except exceptions.TimeoutException:
            self.log.error("machine.send_keys: Timeout Error")

        except Exception:
            self.log.error("machine.send_keys: Unknown Error")
            raise Exception
    
    def keyboard(self, argv:[str]):
        """An action state - keyboard
        Keyboard-in values given the <operation> and <key_values>

        Parameters
        ----------
        argv: [str]
            A list of tuple2s, which contains the operation value and key_values value
        """
        try:
            chain = ActionChains(self.driver)
            for arg in argv:
                try:
                    operation = arg[0]
                    key_values = constant.KEYS.get(arg[1], arg[1])
                    if operation == "KEY_DOWN":
                        chain.key_down(key_values)
                    elif operation == "KEY_UP":
                        chain.key_up(key_values)
                    else:
                        chain.send_keys(key_values)
                
                except IndexError:
                    self.log.error("machine.keyboard: Index Error")
                    raise IndexError
            
            chain.perform()

        except Exception:
            self.log.error("machine.keyboard: Unknown Error")
            raise Exception
    
    def open(self, argv:[str]):
        """An action state - open
        Open the file stream given a <filepath>

        Parameters
        ----------
        argv: [str]
            A string, which contains the filepath value
        """
        try:
            self.filepath = argv[0]
            if os.path.isfile(self.filepath):
                with open(self.filepath, "r") as f:
                    self.fstream = "".join( f.readlines() )
            else:
                self.fstream = ""
            
        except IndexError:
            self.log.error("machine.open: Index Error")
            raise IndexError

        except Exception:
            self.log.error("machine.open: Unknown Error")
            raise Exception

    def close(self, argv:[str]=None):
        """An action state - close
        Flush contents of the file stream to the <filepath>

        """
        try:
            with open(self.filepath, "w") as f:
                f.write(self.fstream)
            self.fstream = ""

        except Exception:
            self.log.error("machine.close: Unknown Error")
            raise Exception
    
    def write(self, argv:[str]):
        """An action state - write
        Write/Append <values> to the file stream

        Parameters
        ----------
        argv: [str]
            A string, which contains the 'values' value
        """
        print()

    def find(self, argv:[str]):
        """An action state - find
        Find and append <text> value from <xpath> element, else append <default> value
        Format the <text> value to be of the form <statement>

        Parameters
        ----------
        argv: [str]
            A tuple3, which contains the xpath value, statement value and default value
        """
        print()
