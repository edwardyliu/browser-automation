# == Import(s) ==
# => Local
from . import utils
from . import config

# => System
import re
from dataclasses import dataclass

# => External
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# == Data Model(s) ==
@dataclass(frozen=True)
class Command:
    """Define a Command:
    
    Execute a command
    """
    label: str
    target: str
    argv: list

@dataclass(frozen=True)
class Sequence:
    """Define a Sequence

    A sequence is a list of Command(s) to be executed linearly
    """
    name: str
    env: str
    cmds: list

# == Data Class(es) ==
class Worker(object):
    
    def __init__(self, uid:str, driver:webdriver):
        """Define a Worker

        """

        self.log = utils.get_logger(uid)
        self.driver = driver
    
    def load(self, sequence:Sequence):
        """Load a command sequence

        """

        self.sequence = sequence
        self.log.info(f"loaded: {self.sequence.env} | {self.sequence.name}")
    
    def push(self, cmd:Command):
        """Push (i.e. append) a new command into the command sequence
        
        Parameters
        ----------
        cmd: Command
            A command object
        """

        self.sequence.cmds.append(cmd)
    
    def pop(self)->Command:
        """Pop the last command away from the command sequence
        
        Returns
        -------
        Command: The popped command object
        """

        return self.sequence.cmds.pop()

    def run(self)->dict:
        """Run command sequence
        
        Returns
        -------
        str: A dictionary of key-value pairs
            key - XPATH
            value - A comma separated list of strings
        """

        self.stdout = {}
        for cmd in self.sequence.cmds: getattr(self, cmd.label)(target=cmd.target, argv=cmd.argv)
        return self.stdout
    
    def find_element_by_xpath(self, target:str):
        """Find element by XPATH

        Returns
        -------
        element: A selenium webdriver element
        """

        return self.driver.find_element_by_xpath(target)

    def find_elements_by_xpath(self, target:str)->list:
        """Find element by XPATH

        Returns
        -------
        list: A list of selenium webdriver element(s)
        """

        return self.driver.find_elements_by_xpath(target)

    def get(self, target:str, argv:list=None):
        """Get URL page

        Parameters
        ----------
        target: str
            A URL string
        argv: [str]
            A list of string values
        """

        self.driver.get(target)

    def click(self, target:str=None, argv:list=None):
        """Click an element

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem.is_displayed(): elem.click()
        else: ActionChains(self.driver).click().perform()

    def click_and_hold(self, target:str=None, argv:list=None):
        """Click an element and hold

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem.is_displayed(): ActionChains(self.driver).click_and_hold(on_element=elem).perform()
        else: ActionChains(self.driver).click_and_hold().perform()
    
    def release(self, target:str=None, argv:list=None):
        """Release click (if any)

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        ActionChains(self.driver).release().perform()

    def context_click(self, target:str=None, argv:list=None):
        """Context click (i.e. right click) an element

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem.is_displayed(): ActionChains(self.driver).context_click(on_element=elem).perform()
        else: ActionChains(self.driver).context_click().perform()
    
    def double_click(self, target:str=None, argv:list=None):
        """Double click an element

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem.is_displayed(): ActionChains(self.driver).double_click(on_element=elem).perform()
        else: ActionChains(self.driver).double_click().perform()
    
    def drag_and_drop(self, target:str, argv:list):
        """Drag and drop from <source> to <dest> (i.e argv[0])

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        try:
            source = self.find_element_by_xpath(target)
            dest = self.find_element_by_xpath(argv[0])
            if source.is_displayed() and dest.is_displayed(): ActionChains(self.driver).drag_and_drop(source=source, target=dest).perform()
            
        except IndexError:
            self.log.error("worker.drag_and_drop: Index Error")
            self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")

    def drag_and_drop_by_offset(self, target:str, argv:list):
        """Drag and drop from <source> to <xoffset>, <yoffset> (i.e argv[0])

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        try:
            source = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if source.is_displayed(): ActionChains(self.driver).drag_and_drop_by_offset(source=source, xoffset=xoffset, yoffset=yoffset).perform()
            
        except IndexError:
            self.log.error("worker.drag_and_drop_by_offset: Index Error")
            self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
    
    def move_to_element(self, target:str, argv:list=None):
        """Move cursor to element

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        elem = self.find_element_by_xpath(target)
        if elem.is_displayed(): ActionChains(self.driver).move_to_element(to_element=elem).perform()
        
    def move_to_element_with_offset(self, target:str, argv:list):
        """Move cursor to element with offset

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        try:
            elem = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if elem.is_displayed(): ActionChains(self.driver).move_to_element_with_offset(to_element=elem, xoffset=xoffset, yoffset=yoffset).perform()

        except IndexError:
            self.log.error("worker.move_to_element_with_offset: Index Error")
            self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
    
    def move_by_offset(self, target:str, argv:list):
        """Move cursor to offset

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        try:
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            ActionChains(self.driver).move_by_offset(xoffset=xoffset, yoffset=yoffset).perform()

        except IndexError:
            self.log.error("worker.move_by_offset: Index Error")
            self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
    
    def send_keys(self, target:str, argv:list):
        """Send keys

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [dict]
            A list of tuple2 string values
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem.is_displayed():
                ac = ActionChains(self.driver)

                for arg in argv:
                    try:
                        if arg[0] == "KEY_DOWN": ac.key_down(config.SPECIAL_KEYS.get(arg[1], arg[1]), element=elem)
                        elif arg[0] == "KEY_UP": ac.key_up(config.SPECIAL_KEYS.get(arg[1], arg[1]), element=elem)
                        else: ac.send_keys_to_element(elem, config.SPECIAL_KEYS.get(arg[1], arg[1]))
                    
                    except IndexError:
                        self.log.error("worker.send_keys: Index Error")
                        self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
                
                ac.perform()
            
        else:
            ac = ActionChains(self.driver)

            for arg in argv:
                try:
                    if arg[0] == "KEY_DOWN": ac.key_down(config.SPECIAL_KEYS.get(arg[1], arg[1]))
                    elif arg[0] == "KEY_UP": ac.key_up(config.SPECIAL_KEYS.get(arg[1], arg[1]))
                    else: ac.send_keys(config.SPECIAL_KEYS.get(arg[1], arg[1]))
                
                except IndexError:
                    self.log.error("worker.send_keys: Index Error")
                    self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
            
            ac.perform()
    
    def pause(self, target:str, argv:list):
        """Pause webdriver

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        try:
            seconds = float(argv[0])
            ActionChains(self.driver).pause(seconds).perform()

        except IndexError:
            self.log.error("worker.pause: Index Error")
            self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
    
    def wait(self, target:str, argv:list):
        """Wait for expected condition

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        try:
            operation = argv[0]
            condition = config.EXPECTED_CONDITIONS.get(argv[1])

            if condition:
                result = utils.get_parsed_expected_condition(self.driver, target, condition)
                if operation == "UNTIL_NOT": WebDriverWait(self.driver, timeout=config.TIMEOUT).until_not(condition[0](result))
                else: WebDriverWait(self.driver, timeout=config.TIMEOUT).until(condition[0](result))

        except IndexError:
            self.log.error("worker.wait: Index Error")
            self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")

        except ValueError:
            self.log.error("worker.wait: Value Error")
            self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
        
        except exceptions.TimeoutException:
            self.log.error("worker.wait: Timeout Exception")
    
    def find(self, target:str, argv:list=None):
        """Find an element and retrieve its text value

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """
        
        self.stdout[target] = ""
        
        elem = self.find_element_by_xpath(target)
        if elem.is_displayed(): self.stdout[target] = elem.text
    
    def find_all(self, target:str, argv:list=None):
        """Find all elements and retrieve their text values

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            A list of string values
        """

        self.stdout[target] = ""

        elems = self.find_elements_by_xpath(target)
        lst = []
        for elem in elems:
            if elem.is_displayed():
                lst.append(elem.text)
        if lst: self.stdout[target] = ", ".join(lst)

    def printf(self, target:str, argv:list=None):
        """Find all elements and retrieve their text values

        Parameters
        ----------
        target: str
            A formatted string
        argv: [str]
            A list of string values
        """

        key = utils.get_next_stdout(self.stdout)
        self.stdout[key] = ""
        
        if target:
            for idx, elem in enumerate(re.findall(config.POSITIONAL, target)): 
                try: target.replace(elem, argv[idx])
                except IndexError:
                    self.log.error("worker.printf: Index Error | argument index #{idx}")
                    self.log.info(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")

            for elem in re.findall(config.FIND, target):
                xpath = elem[2:-1]
                self.find(xpath)
                target.replace(elem, self.stdout[xpath])
            
            for elem in re.findall(config.FIND_ALL, target):
                xpath = elem[2:-1]
                self.find_all(xpath)
                target.replace(elem, self.stdout[xpath])
            
            self.stdout[key] = target
    