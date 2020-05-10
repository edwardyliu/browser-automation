# project/server/tasks/ina/driver.py

# == Import(s) ==
# => Local
from . import utils
from . import config
from . import models

# => System
import re
import json

# => External
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# == Object Definition ==
class Driver(object):
    """Define a Driver
    
    A Selenium WebDriver Instance
    """

    def __init__(self, uid:str):
        self.uid = uid
        self.log = utils.get_logger(f"ina.driver.{self.uid}")
        self.driver = utils.get_webdriver()

    def __del__(self):
        self.driver.quit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__del__()
    
    def __str__(self):
        return f"INA.Driver(uid={self.uid})"

    # == Getter(s) ==
    def id(self)->str:
        if hasattr(self, "lut"): return self.lut.get('usrId')
        else: return None
    
    def key(self)->models.Key: 
        if hasattr(self, "task"): return self.task.key 
        else: return None

    # == Setter(s) ==
    def assign(self, task:models.Task):
        """Assign task to driver

        """

        self.reset()
        self.task = task
        self.log.debug(f"assigned: {self.task}")

    def reset(self):
        """Clean state information

        """

        self.lut = {}
        self.results = {}
    
    # == Functional ==
    def run(self, lut:dict=None)->dict:
        """Run (i.e. work) on the task
        
        Parameters
        ----------
        lut: dict, optional
            A look-up table

        Returns
        -------
        str: A dictionary of key-value pairs generated from 'printf' commands
            key - ${r"([0-9]+)"}
            value - a formatted string
        """

        self.lut = lut
        for cmd in self.task.cmds: getattr(self, cmd.label.lower())(target=cmd.target, argv=cmd.argv)
        return self.results
    
    def find_element_by_xpath(self, target:str):
        """Find element by XPATH

        Parameters
        ----------
        target: str
            The XPATH value

        Returns
        -------
        WebElement: A Selenium WebElement
        """

        elem = None
        try: elem = self.driver.find_element_by_xpath(target)
        except exceptions.NoSuchElementException:
            self.log.error("find_element_by_xpath: No Such Element Exception")
            self.log.error(f"invalid task definition: {self.task}")
        
        return elem

    def find_elements_by_xpath(self, target:str)->list:
        """Find element by XPATH

        Parameters
        ----------
        target: str
            The XPATH value

        Returns
        -------
        list: A list of Selenium WebElements
        """

        elems = []
        try: elems = self.driver.find_elements_by_xpath(target)
        except exceptions.NoSuchElementException:
            self.log.error("find_elements_by_xpath: No Such Element Exception")
            self.log.error(f"invalid task definition: {self.task}")

        return elems

    def find(self, target:str)->str:
        """Find the first WebElement by XPATH and retrieve its text value

        Parameters
        ----------
        target: str
            The XPATH value
        
        Returns
        -------
        str: WebElement.text
        """
        
        res = ""
        elem = self.find_element_by_xpath(target)
        if elem: res = elem.text
        
        return res

    def find_all(self, target:str)->str:
        """Find all WebElements by XPATH and retrieve their text values

        Parameters
        ----------
        target: str
            The XPATH value
        
        Returns
        -------
        str: A comma separated string of WebElement.text
        """

        lst = []
        elems = self.find_elements_by_xpath(target)
        for elem in elems:
            if elem: lst.append(elem.text)
        
        return ", ".join(lst)

    def peek(self, target:str)->str:
        """Peek into the look-up table and if not found, peek into the web page

        Parameters
        ----------
        target: str
            A key value
        
        Returns
        -------
        str: The look-up result
        """

        if self.lut and self.lut.get(target): 
            res = self.lut[target]
            if isinstance(res, str): return res
            elif isinstance(res, list): return ", ".join(str(res))
            elif isinstance(res, dict): return json.dumps(str(res))
            else: 
                try: return str(res)
                except Exception: return f"ERROR: Cannot STRINGIFY Type({type(res)})"
        else: return self.find(target)
    
    def scan(self, fmt:str, argv:list=None)->str:
        """Scan: parse the input arguments into a formatted string

        Parameters
        ----------
        fmt: str
            The string format
        argv: [str]
            A list of positional arguments
            
        Returns
        -------
        str: The formatted string
        """
        
        for placeholder in re.findall(config.POSITIONAL, fmt):
            value = placeholder[2:-1]
            if value == config.LUTV: fmt = fmt.replace(placeholder, json.dumps(self.lut))
            elif value == config.ARGV:
                if argv: fmt = fmt.replace(placeholder, ", ".join(argv))
                else: fmt = fmt.replace(placeholder, "None")
            elif value.isdigit() and argv:
                try: fmt = fmt.replace(placeholder, argv[int(value)-1])
                except IndexError: 
                    self.log.error("scan: Index Error")
                    self.log.error(f"invalid task definition: {self.task}")
                    raise IndexError(f"ina.driver.scan: Index Error - {argv}")
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

        try: 
            self.driver.get(target)
            self.pause(config.DEFAULT_WAIT)
        
        except exceptions.InvalidArgumentException:
            self.log.error(f"get: Invalid Argument Exception - Malformed URL - '{target}' is not a valid URL")
            self.log.error(f"invalid task definition: {self.task}")

        except exceptions.WebDriverException:
            self.log.error("get: WebDriver Exception - Reached Error Page")
            self.log.error(f"invalid task definition: {self.task}")

    def refresh(self, target:str=None, argv:list=None):
        """Refresh current web page

        """

        self.driver.refresh()
    
    def click(self, target:str=None, argv:list=None):
        """Click a WebElement

        Parameters
        ----------
        target: str, optional
            The XPATH value
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).click(on_element=elem).perform()
        else: ActionChains(self.driver).click().perform()

    def click_and_hold(self, target:str=None, argv:list=None):
        """Click and hold a WebElement

        Parameters
        ----------
        target: str, optional
            The XPATH value
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).click_and_hold(on_element=elem).perform()
        else: ActionChains(self.driver).click_and_hold().perform()
    
    def release(self, target:str=None, argv:list=None):
        """Release mouse click

        Parameters
        ----------
        target: str, optional
            The XPATH value
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).release(on_element=elem).perform()
        else: ActionChains(self.driver).release().perform()

    def context_click(self, target:str=None, argv:list=None):
        """Context click (i.e. right-click) a WebElement

        Parameters
        ----------
        target: str, optional
            The XPATH value
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: ActionChains(self.driver).context_click(on_element=elem).perform()
        else: ActionChains(self.driver).context_click().perform()
    
    def double_click(self, target:str=None, argv:list=None):
        """Double click a WebElement

        Parameters
        ----------
        target: str, optional
            The XPATH value
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
            An XPATH value, the source WebElement
        argv: [str]
            An XPATH value, the destination WebElement
        """

        try:
            src = self.find_element_by_xpath(target)
            dest = self.find_element_by_xpath(argv[0])
            if src and dest: ActionChains(self.driver).drag_and_drop(source=src, target=dest).perform()
            
        except IndexError:
            self.log.error(f"drag_and_drop: Index Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(f"ina.driver.drag_and_drop: Index Error - {argv}")

    def drag_and_drop_by_offset(self, target:str, argv:list):
        """Drag and drop from <source> (i.e. target) to <xoffset>, <yoffset> (i.e. argv[0] & argv[1])

        Parameters
        ----------
        target: str
            The XPATH value
        argv: [str]
            The x & y offsets
        """

        try:
            src = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if src: ActionChains(self.driver).drag_and_drop_by_offset(source=src, xoffset=xoffset, yoffset=yoffset).perform()
            
        except IndexError:
            self.log.error("drag_and_drop_by_offset: Index Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(f"ina.driver.drag_and_drop_by_offset: Index Error - {argv}")
    
    def move_to_element(self, target:str, argv:list=None):
        """Move mouse cursor to WebElement

        Parameters
        ----------
        target: str
            The XPATH value
        """

        elem = self.find_element_by_xpath(target)
        if elem: ActionChains(self.driver).move_to_element(to_element=elem).perform()
        
    def move_to_element_with_offset(self, target:str, argv:list):
        """Move mouse cursor to WebElement plus offset

        Parameters
        ----------
        target: str
            The XPATH value
        argv: [str]
            The x & y offsets
        """

        try:
            elem = self.find_element_by_xpath(target)
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            if elem: ActionChains(self.driver).move_to_element_with_offset(to_element=elem, xoffset=xoffset, yoffset=yoffset).perform()

        except IndexError:
            self.log.error("move_to_element_with_offset: Index Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(f"ina.driver.move_to_element_with_offset: Index Error - {argv}")
    
    def move_by_offset(self, target:str, argv:list):
        """Move mouse cursor to offset

        Parameters
        ----------
        argv: [str]
            The x & y offsets
        """

        try:
            xoffset = int(argv[0])
            yoffset = int(argv[1])
            ActionChains(self.driver).move_by_offset(xoffset=xoffset, yoffset=yoffset).perform()

        except IndexError:
            self.log.error("move_by_offset: Index Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(f"ina.driver.move_by_offset: Index Error - {argv}")
    
    def send_keys(self, target:str, argv:list):
        """Send keys
        NOTE. Supports sending special keyboard characters e.g. ${ENTER}, ${ALT}, ${SHIFT}, etc.
        
        Parameters
        ----------
        target: str, optional
            The XPATH value
        argv: [tuple2]
            A list of tuple2 string values
            e.g. [("KEY_DOWN", "${SHIFT}"), "uppercase", ("KEY_UP", "${SHIFT}")]
        """

        if target:
            elem = self.find_element_by_xpath(target)
            if elem: utils.send_keys(self.driver, elem, argv)
        else: utils.send_keys(self.driver, None, argv)
    
    def pause(self, target:str, argv:list=None):
        """Pause the WebDriver instance

        Parameters
        ----------
        target: str
            A float, the number of seconds to pause
        """
        
        try:
            seconds = float(target)
            ActionChains(self.driver).pause(seconds).perform()

        except ValueError:
            self.log.error("pause: Value Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise ValueError(f"ina.driver.pause: Value Error - {target}")
    
    def wait(self, target:str, argv:list)->bool:
        """Wait for an expected condition

        Parameters
        ----------
        target: str
            The XPATH value, an Integer value, or a URL string
        argv: [str]
            A tuple2 of strings containing the operation and expected condition
        """

        try:
            operation = argv[0]
            expected_condition = config.EXPECTED_CONDITIONS.get(argv[1])

            if expected_condition:
                res = utils.parse_expected_condition(self.driver, target, expected_condition[1])
                if operation == "UNTIL_NOT": WebDriverWait(self.driver, timeout=config.DEFAULT_TIMEOUT).until_not(expected_condition[0](res))
                else: WebDriverWait(self.driver, timeout=config.DEFAULT_TIMEOUT).until(expected_condition[0](res))
                
                return True
            else:
                self.log.error("wait: Value Error")
                self.log.error(f"invalid task definition: {self.task}")
                raise ValueError(f"ina.driver.wait: Value Error - {argv[1]}")

        except IndexError:
            self.log.error("wait: Index Error")
            self.log.error(f"invalid task definition: {self.task}")
            raise IndexError(f"ina.driver.wait: Index Error - {argv}")
        
        except exceptions.TimeoutException:
            self.log.error("wait: Timeout Exception")
            return False
    
    # => Dynamic Command Function(s): Commands w/ User-Specified Input(s)
    def dget(self, target:str, argv:list=None):
        """Dynamic get
        Supports user dictionary & web element look-ups.

        Parameters
        ----------
        target: str
            The string format
        """

        self.get(self.scan(target))

    def dclick(self, target:str, argv:list=None):
        """Dynamic click
        Supports user dictionary & web element look-ups.

        Parameters
        ----------
        target: str
            The string format
        """

        self.click(self.scan(target))

    def dsend_keys(self, target:str, argv:list):
        """Dynamic send keys
        NOTE. Supports sending user dictionary & web element look-ups. 
        However, does not support keyboard logic & special characters.

        Parameters
        ----------
        target: str, optional
            The XPATH value
        argv: [str]
            A list of strings
        """

        values = map(lambda arg: self.scan(arg), filter(lambda arg: isinstance(arg, str), argv))
        if target:
            elem = self.find_element_by_xpath(target)
            if elem: utils.send_keys(self.driver, elem, values)
        else: utils.send_keys(self.driver, None, values)
    
    def printf(self, target:str, argv:list=None):
        """Generate a formatted string
        Find & replace all special sequences and generate a formatted string.

        Parameters
        ----------
        target: str
            The string format
        argv: [str]
            A list of positional arguments
        """
        
        argvkey = utils.next_argv_key(self.results)
        self.results[argvkey] = ""
        
        if target: self.results[argvkey] = self.scan(fmt=target, argv=argv)
    
    # => Popular Command Combination(s)
    def write(self, target:str, argv:list=None):
        """Write: a combination of self.wait(target) & self.dsend_keys(target, argv)

        Parameters
        ----------
        target: str
            The XPATH value
        argv: [str]
            A list of strings
        """
        
        if self.wait(target, ("UNTIL", "VISIBILITY_OF_ELEMENT_LOCATED")): self.dsend_keys(target, argv)
        