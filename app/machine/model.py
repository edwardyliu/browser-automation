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

    def __init__(self, uid:str, driver:webdriver, actions:list, path:str=None):
        self.log = utils.get_logger(uid)
        self.driver = driver
        self.actions = actions
        self.path = path

        self.size = len(self.actions) - 1
        self.counter = 0
    
    def __enter__(self):
        self.stream = ""
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.path and self.stream: self.close()

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
        # info
        self.log.info(f"machine.idle: ")
        
        # wait
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
            # extract
            decimal = float(argv[0])
            
            # info
            self.log.info(f"machine.wait: {decimal}")

            # wait
            time.sleep(decimal)

        except IndexError:
            self.idle()

        except ValueError:
            self.log.error("machine.wait: Value Error")
            raise ValueError

    def get(self, argv:[str]):
        """An action state - get
        Get <url> page

        Parameters
        ----------
        argv: [str]
            A string, which contains the url value
        """
        try:
            # extract
            url = argv[0]

            # info
            self.log.info(f"machine.get: {url}")

            # get & wait
            self.driver.get(url)
            time.sleep(constant.GET)
        
        except IndexError:
            self.log.error("machine.get: Index Error")
            raise IndexError
        
        except Exception:
            self.log.error("machine.get: Unknown Error")
            raise Exception

    def get_elem(self, argv:[str]):
        """An action state - get_elem
        Get text value of first <xpath> element

        Parameters
        ----------
        argv: [str]
            A string, which contains the xpath value

        Returns
        -------
        string:
            The text value
        """
        print()

    def get_elems(self, argv:[str]):
        """An action state - get_elem
        Get text value of all <xpath> element(s)

        Parameters
        ----------
        argv: [str]
            A string, which contains the xpath value
        
        Returns
        -------
        list:
            A list of text value(s)
        """
        print()

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
                # info
                self.log.info(f"machine.click: {xpath}")
                
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
                # info
                self.log.info(f"machine.double_click: {xpath}")

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

            # info
            self.log.info(f"machine.send_keys: {xpath}, {values}")

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
                    # extract
                    operation = arg[0]
                    key_values = constant.KEYS.get(arg[1], arg[1])

                    # info
                    self.log.info(f"machine.keyboard: {operation}, {key_values}")

                    # append corresponding action
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
    
    def new(self, argv:[str]):
        """An action state - create
        New file stream and file <path>

        Parameters
        ----------
        argv: [str]
            A string, which contains the file path value
        """
        try:
            # info
            self.log.info(f"machine.new: ")

            # init
            self.stream = ""
            self.path = argv[0]
            
        except IndexError:
            self.log.error("machine.new: Index Error")
            raise IndexError

        except Exception:
            self.log.error("machine.new: Unknown Error")
            raise Exception

    def flush(self, argv:[str]=None):
        """An action state - flush
        Flush file stream to file <path>

        """
        try:
            # info
            self.log.info(f"machine.flush: {self.path}, {self.stream}")

            # flush
            with open(self.path, "a") as f:
                f.write(self.stream)
            self.stream = ""
        
        except Exception:
            self.log.error("machine.flush: Unknown Error")
            raise Exception

    def open(self, argv:[str]):
        """An action state - open
        Open & load content from file <path> into file stream

        Parameters
        ----------
        argv: [str]
            A string, which contains the file path value
        """
        try:
            # extract
            self.path = argv[0]

            # open & read
            if os.path.isfile(self.path):
                with open(self.path, "r") as f:
                    self.stream = "".join( f.readlines() )
            else:
                self.stream = ""
            
        except IndexError:
            self.log.error("machine.open: Index Error")
            raise IndexError

        except Exception:
            self.log.error("machine.open: Unknown Error")
            raise Exception

    def close(self, argv:[str]=None):
        """An action state - close
        Close (i.e. overwrite) file <path> with file stream content 

        """
        try:
            # open & write
            with open(self.path, "w") as f:
                f.write(self.stream)
            self.stream = ""

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
