# == Import(s) ==
# => Local
from . import config
from . import utils
from . import models

# => System
import re

# => External
import json
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# == Object Class ==
class Worker(object):
    """Define a Worker
    
    """

    def __init__(self, uid:str):
        self.uid = uid
        self.log = utils.get_logger(self.uid)
        self.driver = utils.get_webdriver()

    def __del__(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()
    
    def __str__(self):
        return f"Worker: {self.uid}"

    # == Getter(s) ==
    def key(self)->models.Key: 
        if hasattr(self, "task"): return self.task.key 
        else: return None

    # == Setter(s) ==
    def assign(self, task:models.Task):
        """Assign worker to a task

        """

        self.reset()
        self.task = task
        self.log.info(f"assigned with: {self.task}")

    def reset(self):
        """Reset any saved states

        """

        self.tbl = {}
        self.results = {}

    # == Functional ==
    def run(self, tbl:dict=None)->dict:
        """Run command task
        
        Parameters
        ----------
        tbl: dict
            A look-up table

        Returns
        -------
        str: A dictionary of key-value pairs
            key - XPATH
            value - A comma separated list of strings
        """

        self.tbl = tbl
        for cmd in self.task.cmds: getattr(self, cmd.label.lower())(target=cmd.target, argv=cmd.argv)
        return self.results
    
    def find_element_by_xpath(self, target:str):
        """Find element by XPATH

        Returns
        -------
        WebElement: A selenium web element object
        """

        elem = None
        try: elem = self.driver.find_element_by_xpath(target)
        except exceptions.NoSuchElementException:
            self.log.error("worker.find_element_by_xpath: No Such Element Exception")
            self.log.error(f"invalid task definition: {self.task}")
        
        return elem

    def find_elements_by_xpath(self, target:str)->list:
        """Find element by XPATH

        Returns
        -------
        list: A list of selenium web element objects
        """

        elems = []
        try: elems = self.driver.find_elements_by_xpath(target)
        except exceptions.NoSuchElementException:
            self.log.error("worker.find_elements_by_xpath: No Such Element Exception")
            self.log.error(f"invalid task definition: {self.task}")

        return elems

    def find(self, target:str)->str:
        """Find a web element and retrieve its text value

        Parameters
        ----------
        target: str
            An XPATH value
        
        Returns
        -------
        str: WebElement.text
        """
        
        res = ""
        elem = self.find_element_by_xpath(target)
        if elem: res = elem.text
        
        return res

    def find_all(self, target:str)->str:
        """Find all web elements and retrieve their text values

        Parameters
        ----------
        target: str
            An XPATH value
        
        Returns
        -------
        str: A comma separated list of WebElement.text
        """

        lst = []
        elems = self.find_elements_by_xpath(target)
        for elem in elems:
            if elem: lst.append(elem.text)
        
        return ", ".join(lst)

    def peek(self, target:str)->str:
        """Peek the look-up table; if not found, peek the web page

        Parameters
        ----------
        target: str
            The key
        
        Returns
        -------
        str: The value
        """

        if self.tbl and self.tbl.get(target): 
            res = self.tbl[target]
            if isinstance(res, str): return res
            elif isinstance(res, list): return ", ".join(str(res))
            elif isinstance(res, dict): return json.dumps(str(res))
            else: 
                try: return str(res)
                except Exception: return "{ERROR: CANNOT STRINGIFY}"
        else: return self.find(target)
    
    def scan(self, fmt:str, argv:list=None)->str:
        """Scan and format the raw string

        Parameters
        ----------
        fmt: str
            The raw string
        argv: [str]
            A list of positional arguments
            
        Returns
        -------
        str: The formatted string
        """
        
        for placeholder in re.findall(config.POSITIONAL, fmt):
            value = placeholder[2:-1]
            if value == config.TBLV: fmt = fmt.replace(placeholder, json.dumps(self.tbl))
            elif value == config.ARGV:
                if argv: fmt = fmt.replace(placeholder, ", ".join(argv))
                else: fmt = fmt.replace(placeholder, "None")
            elif value.isdigit() and argv:
                try: fmt = fmt.replace(placeholder, argv[int(value)-1])
                except IndexError: 
                    self.log.error("worker.scan: Index Error")
                    self.log.error(f"invalid task definition: {self.task}")
                    raise IndexError(argv)
            elif value[0] == config.FINDV: fmt = fmt.replace(placeholder, self.find_all(value[1:]))
            else: fmt = fmt.replace(placeholder, self.peek(value))
        
        return fmt
    
    # == Command Function(s) ==
    def get(self, target:str, argv:list=None):
        """Get URL page

        Parameters
        ----------
        target: str
            A URL string
        """

        try: self.driver.get(target); self.pause(config.WAIT)

        except exceptions.InvalidArgumentException:
            self.log.error(f"worker.get: Invalid Argument Exception - Malformed URL | '{target}' is not a valid URL")
            self.log.error(f"invalid task definition: {self.task}")

        except exceptions.WebDriverException:
            self.log.error("worker.get: WebDriver Exception - Reached error page")
            self.log.error(f"invalid task definition: {self.task}")

    def refresh(self, target:str=None, argv:list=None):
        """Refresh the page

        """

        self.driver.refresh()
    
    def click(self, target:str=None, argv:list=None):
        """Click a web element

        Parameters
        ----------
        target: str
            An XPATH value (if any)
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).click(on_element=elem).perform()
        else: ActionChains(self.driver).click().perform()

    def click_and_hold(self, target:str=None, argv:list=None):
        """Click and hold a web element

        Parameters
        ----------
        target: str
            An XPATH value (if any)
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).click_and_hold(on_element=elem).perform()
        else: ActionChains(self.driver).click_and_hold().perform()
    
    def release(self, target:str=None, argv:list=None):
        """Release click

        Parameters
        ----------
        target: str
            An XPATH value (if any)
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).release(on_element=elem).perform()
        else: ActionChains(self.driver).release().perform()

    def context_click(self, target:str=None, argv:list=None):
        """Context click (i.e. right click) a web element

        Parameters
        ----------
        target: str
            An XPATH value (if any)
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).context_click(on_element=elem).perform()
        else: ActionChains(self.driver).context_click().perform()
    
    def double_click(self, target:str=None, argv:list=None):
        """Double click a web element

        Parameters
        ----------
        target: str
            An XPATH value (if any)
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).double_click(on_element=elem).perform()
        else: ActionChains(self.driver).double_click().perform()
    
    def drag_and_drop(self, target:str, argv:list):
        """Drag and drop from <source> (i.e. target) to <dest> (i.e. argv[0])

        Parameters
        ----------
        target: str
            An XPATH value, the source
        argv: [str]
            An XPATH value, the destination
        """

        try:
            src = self.find_element_by_xpath(target)
            dest = self.find_element_by_xpath(argv[0])
            if src and dest: ActionChains(self.driver).drag_and_drop(source=src, target=dest).perform()
            
        except IndexError:
            self.log.error("worker.drag_and_drop: Index Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(argv)

    def drag_and_drop_by_offset(self, target:str, argv:list):
        """Drag and drop from <source> (i.e. target) to <xoffset>, <yoffset> (i.e. argv[0] & argv[1])

        Parameters
        ----------
        target: str
            An XPATH value, the source
        argv: [str]
            The x & y offset
        """

        try:
            src = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if src: ActionChains(self.driver).drag_and_drop_by_offset(source=src, xoffset=xoffset, yoffset=yoffset).perform()
            
        except IndexError:
            self.log.error("worker.drag_and_drop_by_offset: Index Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(argv)
    
    def move_to_element(self, target:str, argv:list=None):
        """Move mouse cursor to web element

        Parameters
        ----------
        target: str
            An XPATH value
        """

        elem = self.find_element_by_xpath(target)
        if elem: ActionChains(self.driver).move_to_element(to_element=elem).perform()
        
    def move_to_element_with_offset(self, target:str, argv:list):
        """Move mouse cursor to web element plus offset

        Parameters
        ----------
        target: str
            An XPATH value
        argv: [str]
            The x & y offset
        """

        try:
            elem = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if elem: ActionChains(self.driver).move_to_element_with_offset(to_element=elem, xoffset=xoffset, yoffset=yoffset).perform()

        except IndexError:
            self.log.error("worker.move_to_element_with_offset: Index Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(argv)
    
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
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(argv)
    
    def send_keys(self, target:str, argv:list):
        """Send keys
        NOTE. Supports special keyboard character e.g. ${ENTER}, ${ALT}, ${SHIFT}, etc.
        
        Parameters
        ----------
        target: str
            An XPATH value, optional
        argv: [tuple2]
            A list of tuple2 string values
            e.g. [("KEY_DOWN", "${SHIFT}"), "uppercase", ("KEY_UP", "${SHIFT}")]
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: utils.send_keys(self.driver, elem, argv)
        else: utils.send_keys(self.driver, None, argv)
    
    def pause(self, target:str, argv:list=None):
        """Pause the WebDriver

        Parameters
        ----------
        target: str
            The number of seconds to pause
        """
        
        try:
            seconds = float(target)
            ActionChains(self.driver).pause(seconds).perform()

        except ValueError:
            self.log.error("worker.pause: Value Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise ValueError(seconds)
    
    def wait(self, target:str, argv:list)->bool:
        """Wait for expected condition

        Parameters
        ----------
        target: str
            An XPATH value, an Integer, or a String
        argv: [str]
            A tuple2 of strings containing the wait operation and expected condition
        """

        try:
            operation = argv[0]
            expected_condition = config.EXPECTED_CONDITIONS.get(argv[1])

            if expected_condition:
                res = utils.parse_expected_condition(self.driver, target, expected_condition[1])
                if operation == "UNTIL_NOT": WebDriverWait(self.driver, timeout=config.TIMEOUT).until_not(expected_condition[0](res))
                else: WebDriverWait(self.driver, timeout=config.TIMEOUT).until(expected_condition[0](res))
                
                return True
            else:
                self.log.error("worker.wait: Value Error")
                self.log.error(f"invalid task definition: {self.task}")
                raise ValueError(argv)

        except IndexError:
            self.log.error("worker.wait: Index Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(argv)
        
        except exceptions.TimeoutException:
            self.log.error("worker.wait: Timeout Exception")
            return False
    
    # => Dynamic Command Function(s): Commands w/ User-Specified Input(s)
    def dget(self, target:str, argv:list=None):
        """Dynamic get URL page

        Parameters
        ----------
        target: str
            A key
        """

        if self.tbl and self.tbl.get(target): self.get(self.tbl[target])

    def dsend_keys(self, target:str, argv:list):
        """Dynamic send keys 
        NOTE. Supports user dictionary & web element look-up. However, does not support keyboard logic & special characters

        Parameters
        ----------
        target: str
            An XPATH value
        argv: [str]
            A list of strings
        """

        values = map(lambda arg: self.scan(arg), filter(lambda arg: isinstance(arg, str), argv))
        if target:
            elem = self.find_element_by_xpath(target)
            if elem: utils.send_keys(self.driver, elem, values)
        else: utils.send_keys(self.driver, None, values)
    
    def printf(self, target:str, argv:list=None):
        """Output a formatted string
        Find & replace all special sequences and output a formatted string

        Parameters
        ----------
        target: str
            The raw string
        argv: [str]
            A list of positional string values
        """
        
        argvkey = utils.next_argv_key(self.results)
        self.results[argvkey] = ""
        
        if target: self.results[argvkey] = self.scan(fmt=target, argv=argv)
    
    # => Popular Command Combination(s)
    def write(self, target:str, argv:list=None):
        """Write: a combination of wait(target) & dsend_keys(target, argv)

        Parameters
        ----------
        target: str
            An XPATH value
        argv: [str]
            A list of strings
        """
        
        if self.wait(target, ("UNTIL", "VISIBILITY_OF_ELEMENT_LOCATED")): self.dsend_keys(target, argv)
        