# == Import(s) ==
# => Local
from . import constant
from . import utils

# => System
import os
import re
import time
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

    def get_page(self, argv:[str]):
        """An action state - get page
        Get page of <url>

        Parameters
        ----------
        argv: [str]
            A string, which contains the url value
        """
        try:
            # extract
            url = argv[0]

            # info
            self.log.info(f"machine.get_page: {url}")

            # get page & wait
            self.driver.get(url)
            time.sleep(constant.GET)
        
        except IndexError:
            self.log.error("machine.get_page: Index Error")
            raise IndexError
        
        except Exception:
            self.log.error("machine.get_page: Unknown Error")
            raise Exception

    def get_elem(self, argv:[str])->str:
        """An action state - get element
        Get text value of first <xpath> element

        Parameters
        ----------
        argv: [str]
            A string, which contains the xpath value

        Returns
        -------
        string:
            A element text value
        """
        try:
            # extract
            xpath = argv[0]

            # info
            self.log.info(f"machine.get_elem: {xpath}")

            # locate
            elem_presence = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.driver, constant.TIMEOUT).until(elem_presence)

            # get element text
            elem = self.driver.find_element_by_xpath(xpath)
            if type(elem) is list:
                return elem[0].text
            else:
                return elem.text

        except IndexError:
            self.log.error("machine.get_elem: Index Error")
            raise IndexError

        except exceptions.TimeoutException:
            return None
        
        except Exception:
            self.log.error("machine.get_elem: Unknown Error")
            raise Exception
        
    def get_elems(self, argv:[str])->[str]:
        """An action state - get elements
        Get text value of all <xpath> element(s)

        Parameters
        ----------
        argv: [str]
            A string, which contains the xpath value
        
        Returns
        -------
        list:
            A list of element text value(s)
        """
        try:
            # extract
            xpath = argv[0]

            # info
            self.log.info(f"machine.get_elems: {xpath}")

            # locate
            elem_presence = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.driver, constant.TIMEOUT).until(elem_presence)

            # get all element text
            elems = self.driver.find_element_by_xpath(xpath)
            if type(elems) is not list:
                elems = [elems]
            
            return list( map(lambda elem: elem.text, elems) )

        except IndexError:
            self.log.error("machine.get_elems: Index Error")
            raise IndexError

        except exceptions.TimeoutException:
            return None
        
        except Exception:
            self.log.error("machine.get_elems: Unknown Error")
            raise Exception

    def click_elem(self, argv:[str]):
        """An action state - click element
        Click first <xpath> element

        Parameters
        ----------
        argv: [str]
            A list of strings, which contains the xpath value(s)
        """
        for xpath in argv:
            try:
                # info
                self.log.info(f"machine.click_elem: {xpath}")
                
                # locate
                elem_presence = EC.presence_of_element_located((By.XPATH, xpath))
                WebDriverWait(self.driver, constant.TIMEOUT).until(elem_presence)

                # click first element
                elem = self.driver.find_element_by_xpath(xpath)
                if type(elem) is list:
                    elem[0].click()
                else:
                    elem.click()

                # wait
                time.sleep(constant.CLICK)

            except exceptions.TimeoutException:
                self.log.error("machine.click_elem: Timeout Error")
            
            except Exception:
                self.log.error("machine.click_elem: Unknown Error")
                raise Exception

    def double_click_elem(self, argv:[str]):
        """An action state - double-click element
        Double-click first <xpath> element

        Parameters
        ----------
        argv: [str]
            A list of strings, which contains the xpath value(s)
        """
        for xpath in argv:
            try:
                # info
                self.log.info(f"machine.double_click_elem: {xpath}")

                # locate
                elem_presence = EC.presence_of_element_located((By.XPATH, xpath))
                WebDriverWait(self.driver, constant.TIMEOUT).until(elem_presence)

                # double-click first element
                elem = self.driver.find_element_by_xpath(xpath)
                if type(elem) is list:
                    elem[0].double_click()
                else:
                    elem.double_click()

                # wait
                time.sleep(constant.DOUBLE_CLICK)

            except exceptions.TimeoutException:
                self.log.error("machine.double_click_elem: Timeout Error")
            
            except Exception:
                self.log.error("machine.double_click_elem: Unknown Error")
                raise Exception

    def send_keys_elem(self, argv:[str]):
        """An action state - send keys to element
        Send-keys <values> to first <xpath> element

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
            self.log.info(f"machine.send_keys_elem: {xpath}, {values}")

            # locate
            elem_presence = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.driver, constant.TIMEOUT).until(elem_presence)

            # send-keys to first element
            elem = self.driver.find_element_by_xpath(xpath)
            if type(elem) is list:
                elem[0].send_keys(values)
            else:
                elem.send_keys(values)
            
        except IndexError:
            self.log.error("machine.send_keys_elem: Index Error")
            raise IndexError
        
        except exceptions.TimeoutException:
            self.log.error("machine.send_keys_elem: Timeout Error")

        except Exception:
            self.log.error("machine.send_keys_elem: Unknown Error")
            raise Exception
    
    def send_keys(self, argv:[str]):
        """An action state - send keys
        Send-keys <operation> and <values>

        Parameters
        ----------
        argv: [str]
            A list of tuple2s, which contains the operation value and 'values' value
        """
        try:
            chain = ActionChains(self.driver)
            for arg in argv:
                try:
                    # extract
                    operation = arg[0]
                    values = constant.KEYS.get(arg[1], arg[1])

                    # info
                    self.log.info(f"machine.send_keys: {operation}, {values}")

                    # append corresponding action
                    if operation == constant.KEY_DOWN:
                        chain.key_down(values)
                    elif operation == constant.KEY_UP:
                        chain.key_up(values)
                    else:
                        chain.send_keys(values)
                
                except IndexError:
                    self.log.error("machine.send_keys: Index Error")
                    raise IndexError
            
            chain.perform()

        except Exception:
            self.log.error("machine.send_keys: Unknown Error")
            raise Exception
    
    def make_file(self, argv:[str]):
        """An action state - make file
        Make a new file: a fresh file stream and a new file <path>

        Parameters
        ----------
        argv: [str]
            A string, which contains the file path value
        """
        try:
            # info
            self.log.info(f"machine.make_file: ")

            # init
            self.stream = ""
            self.path = argv[0]
            
        except IndexError:
            self.log.error("machine.make_file: Index Error")
            raise IndexError

        except Exception:
            self.log.error("machine.make_file: Unknown Error")
            raise Exception

    def flush(self, argv:[str]=None):
        """An action state - flush
        Flush current file stream to file <path>

        """
        try:
            # info
            self.log.info(f"machine.flush: {self.path}\nstream: {self.stream}")

            # flush
            with open(self.path, "a") as f:
                f.write(self.stream)
            self.stream = ""
        
        except Exception:
            self.log.error("machine.flush: Unknown Error")
            raise Exception

    def open_file(self, argv:[str]):
        """An action state - open file
        Open, read & load content from file <path> into file stream

        Parameters
        ----------
        argv: [str]
            A string, which contains the file path value
        """
        try:
            # extract
            self.path = argv[0]

            # info
            self.log.info(f"machine.open_file: {self.path}")

            # open & read
            if os.path.isfile(self.path):
                with open(self.path, "r") as f:
                    self.stream = "".join( f.readlines() )
            else:
                self.stream = ""
            
        except IndexError:
            self.log.error("machine.open_file: Index Error")
            raise IndexError

        except Exception:
            self.log.error("machine.open_file: Unknown Error")
            raise Exception

    def close_file(self, argv:[str]=None):
        """An action state - close file
        Close (i.e. overwrite) content from file stream into file <path>

        """
        try:
            # info
            self.log.info(f"machine.close_file: {self.path}\nstream: {self.stream}")
            
            # open & write
            with open(self.path, "w") as f:
                f.write(self.stream)
            self.stream = ""

        except Exception:
            self.log.error("machine.close_file: Unknown Error")
            raise Exception
    
    def write(self, argv:[str]):
        """An action state - write
        Write <values> value to file stream

        Parameters
        ----------
        argv: [str]
            A string, which contains the 'values' value
        """
        try:
            # extract
            values = argv[0]

            # info
            self.log.info(f"machine.write: {values}")

            # parse
            positional = re.findall(constant.POSITIONAL, values)
            elem = re.findall(constant.ELEM, values)
            elems = re.findall(constant.ELEMS, values)

            for idx, arg in enumerate(positional):
                values = values.replace(arg, argv[idx+1])
            for arg in elem:
                values = values.replace(arg, str(self.get_elem([arg])))
            for arg in elems:
                lst = self.get_elems([arg])
                if lst:
                    values = values.replace(arg, ", ".join(lst))
                else:
                    values = values.replace(arg, "None")

            # append
            self.stream += f"{values}\n"

        except IndexError:
            self.log.error("machine.write: Index Error")
            raise IndexError

        except Exception:
            self.log.error("machine.write: Unknown Error")
            raise Exception
    
    def write_if_else(self, argv:[str]):
        """An action state - write if else
        Write <values> value if <xpath> element is found, else write <default> value

        Parameters
        ----------
        argv: [str]
            A tuple3, which contains the xpath value (i.e. if condition), 'values' value and default value
        """
        try:
            # extract
            xpath = argv[0]
            values = argv[1]
            default = argv[2]

            # info
            self.log.info(f"machine.write_if_else: {xpath}, {values}, default: {default}")

            # locate
            elem_presence = EC.presence_of_element_located((By.XPATH, xpath))
            WebDriverWait(self.driver, constant.TIMEOUT).until(elem_presence)

            # if element was located
            self.write(values)

        except IndexError:
            self.log.error("machine.write_if_else: Index Error")
            raise IndexError
        
        except exceptions.TimeoutException:
            # if element was not located
            self.write([default])

        except Exception:
            self.log.error("machine.write_if_else: Unknown Error")
            raise Exception
