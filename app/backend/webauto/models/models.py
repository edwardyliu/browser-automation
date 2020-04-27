# == Import(s) ==
# => Local
from . import utils
from . import config

# => System
import re
from collections import deque
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

    def __str__(self):
        return f"Command: {self.label}"

@dataclass(frozen=True)
class Sequence:
    """Define a Sequence

    A sequence is a list of Command(s) to be executed linearly
    """

    name: str
    env: str
    cmds: deque

    def __str__(self):
        return f"Sequence: {self.env}, {self.name}"

    def push(self, cmd:Command):
        """Push a new command to the rightmost position

        Parameters
        ----------
        cmd: Command
            A command object
        """

        self.cmds.append(cmd)

    def pushleft(self, cmd:Command):
        """Push a new command to the leftmost position
        
        Parameters
        ----------
        cmd: Command
            A command object
        """

        self.cmds.appendleft(cmd)

    def extend(self, cmds:list):
        """Extend a list of new commands, in order, to the rightmost position
        
        Parameters
        ----------
        cmds: list
            A list of command objects
        """

        self.cmds.extend(cmds)

    def extendleft(self, cmds:list):
        """Extend a list of new commands, in order, to the leftmost position
        
        Parameters
        ----------
        cmds: list
            A list of command objects
        """

        for cmd in reversed(cmds): self.cmds.appendleft(cmd)

    def pop(self)->Command:
        """Pop the rightmost command away from the command list
        
        Returns
        -------
        Command: The popped command object
        """

        return self.cmds.pop()

    def popleft(self)->Command:
        """Pop the leftmost command away from the command list
        
        Returns
        -------
        Command: The popped command object
        """

        return self.cmds.popleft()

# == Data Class(es) ==
class Worker(object):
    """Define a Worker
    
    """

    def __init__(self, uid:str, driver:webdriver):
        self.uid = uid
        self.log = utils.get_logger(self.uid)
        self.driver = driver

    def __del__(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
    
    def __str__(self):
        return f"Worker: {self.uid}"

    def load(self, sequence:Sequence):
        """Load a command sequence

        """

        self.sequence = sequence
        self.log.info(f"loaded: {self.sequence.env} | {self.sequence.name}")

    def run(self)->dict:
        """Run command sequence
        
        Returns
        -------
        str: A dictionary of key-value pairs
            key - XPATH
            value - A comma separated list of strings
        """

        self.stdout = {}
        for cmd in self.sequence.cmds: getattr(self, cmd.label.lower())(target=cmd.target, argv=cmd.argv)
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
        """

        self.driver.get(target)

    def refresh(self, target:str=None, argv:list=None):
        """Refresh the page

        """

        self.driver.refresh()
    
    def click(self, target:str=None, argv:list=None):
        """Click an element

        Parameters
        ----------
        target: str
            An XPATH string (if any)
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem.is_displayed(): ActionChains(self.driver).click(on_element=elem).perform()
        else: ActionChains(self.driver).click().perform()

    def click_and_hold(self, target:str=None, argv:list=None):
        """Click an element and hold

        Parameters
        ----------
        target: str
            An XPATH string (if any)
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem.is_displayed(): ActionChains(self.driver).click_and_hold(on_element=elem).perform()
        else: ActionChains(self.driver).click_and_hold().perform()
    
    def release(self, target:str=None, argv:list=None):
        """Release mouse click

        Parameters
        ----------
        target: str
            An XPATH string (if any)
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem.is_displayed(): ActionChains(self.driver).release(on_element=elem).perform()
        else: ActionChains(self.driver).release().perform()

    def context_click(self, target:str=None, argv:list=None):
        """Context click (i.e. right click) an element

        Parameters
        ----------
        target: str
            An XPATH string (if any)
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
            An XPATH string (if any)
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
            An XPATH string, source
        argv: [str]
            An XPATH string, destination
        """

        try:
            source = self.find_element_by_xpath(target)
            dest = self.find_element_by_xpath(argv[0])
            if source.is_displayed() and dest.is_displayed(): ActionChains(self.driver).drag_and_drop(source=source, target=dest).perform()
            
        except IndexError:
            self.log.error("worker.drag_and_drop: Index Error")
            self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")

    def drag_and_drop_by_offset(self, target:str, argv:list):
        """Drag and drop from <source> to <xoffset>, <yoffset> (i.e argv[0])

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [str]
            The x & y offset
        """

        try:
            source = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if source.is_displayed(): ActionChains(self.driver).drag_and_drop_by_offset(source=source, xoffset=xoffset, yoffset=yoffset).perform()
            
        except IndexError:
            self.log.error("worker.drag_and_drop_by_offset: Index Error")
            self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
    
    def move_to_element(self, target:str, argv:list=None):
        """Move cursor to element

        Parameters
        ----------
        target: str
            An XPATH string
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
            The x & y offset
        """

        try:
            elem = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if elem.is_displayed(): ActionChains(self.driver).move_to_element_with_offset(to_element=elem, xoffset=xoffset, yoffset=yoffset).perform()

        except IndexError:
            self.log.error("worker.move_to_element_with_offset: Index Error")
            self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
    
    def move_by_offset(self, target:str, argv:list):
        """Move cursor to offset

        Parameters
        ----------
        argv: [str]
            The x & y offset
        """

        try:
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            ActionChains(self.driver).move_by_offset(xoffset=xoffset, yoffset=yoffset).perform()

        except IndexError:
            self.log.error("worker.move_by_offset: Index Error")
            self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
    
    def send_keys(self, target:str, argv:list):
        """Send keys

        Parameters
        ----------
        target: str
            An XPATH string
        argv: [dict]
            A list of tuple2 string values
        """

        try:
            if target:
                elem = self.find_element_by_xpath(target)
                if elem.is_displayed():
                    utils.send_keys(self.driver, elem, argv)
            else: utils.send_keys(self.driver, None, argv)
        
        except IndexError:
            self.log.error("worker.send_keys: Index Error")
            self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
        
        except KeyError:
            self.log.error("worker.send_keys: Key Error")
            self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
        
    def pause(self, target:str, argv:list=None):
        """Pause webdriver

        Parameters
        ----------
        target: str
            The number of seconds to pause
        """

        try:
            seconds = float(target)
            ActionChains(self.driver).pause(seconds).perform()

        except IndexError:
            self.log.error("worker.pause: Index Error")
            self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
    
    def wait(self, target:str, argv:list):
        """Wait for expected condition

        Parameters
        ----------
        target: str
            An XPATH string, an Integer, or a String
        argv: [str]
            The operation and expected condition
        """

        try:
            operation = argv[0]
            condition = config.EXPECTED_CONDITIONS.get(argv[1])

            if condition:
                result = utils.parse_expected_condition(self.driver, target, condition[1])
                if operation == "UNTIL_NOT": WebDriverWait(self.driver, timeout=config.TIMEOUT).until_not(condition[0](result))
                else: WebDriverWait(self.driver, timeout=config.TIMEOUT).until(condition[0](result))
        
        except IndexError:
            self.log.error("worker.wait: Index Error")
            self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")

        except ValueError:
            self.log.error("worker.wait: Value Error")
            self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")
        
        except exceptions.TimeoutException:
            self.log.error("worker.wait: Timeout Exception")
    
    def find(self, target:str, argv:list=None):
        """Find an element and retrieve its text value

        Parameters
        ----------
        target: str
            An XPATH string
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
            A list of positional string values
        """

        key = utils.next_dict_key(self.stdout)
        self.stdout[key] = ""
        
        if target:
            for idx, elem in enumerate(re.findall(config.POSITIONAL, target)): 
                try: 
                    if elem == "${@}": target = target.replace(elem, ", ".join(argv or []))
                    else: target = target.replace(elem, argv[idx])
                except IndexError:
                    self.log.error("worker.printf: Index Error | argument index #{idx}")
                    self.log.error(f"invalid sequence definition: {self.sequence.env} | {self.sequence.name}")

            for elem in re.findall(config.FIND, target):
                xpath = elem[2:-1]
                self.find(xpath)
                target = target.replace(elem, self.stdout[xpath])
            
            for elem in re.findall(config.FIND_ALL, target):
                xpath = elem[2:-1]
                self.find_all(xpath)
                target = target.replace(elem, self.stdout[xpath])
            
            self.stdout[key] = target
    